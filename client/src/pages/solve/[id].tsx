import React, { useEffect, useState, useRef } from "react";
import { useRouter } from "next/router";
import { useDispatch, useSelector } from "react-redux";
import stringSimilarity from "string-similarity";
import { RootState } from "@/store";
import {
  fetchSnippet,
  setFetchSnippetStatus,
} from "@/store/snippet_store/actions";
import { addLeaderboardEntry } from "@/store/leaderboard_store/actions";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useSession } from "next-auth/react";
import { fetchUser } from "../../store/user_store/actions";

const SolvePage: React.FC = () => {
  const router = useRouter();
  const { data: session } = useSession();
  const dispatch = useDispatch();
  const { id } = router.query;

  const snippet = useSelector((state: RootState) => state.snippet.snippet);
  const status = useSelector(
    (state: RootState) => state.snippet.fetchSnippetStatus
  );
  const [userInputs, setUserInputs] = useState<string[]>([]);
  const [difficulty, setDifficulty] = useState<number>(5); // default difficulty 5
  const [debouncedDifficulty, setDebouncedDifficulty] =
    useState<number>(difficulty);
  const [answerMatches, setAnswerMatches] = useState<boolean[]>([]); // true/false per answer
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [threshold, setThreshold] = useState<number>(0.5);
  const ifmask = true;
  const userDBData = useSelector((state: RootState) => state.user.user);

  type Result = {
    match: boolean;
    similarity: number;
  };

  useEffect(() => {
    if (session?.user?.email && userDBData?.email !== session?.user?.email) {
      dispatch(fetchUser(session.user.email));
      console.log("dispatch useeffect add snippect");
    }
  }, [session, dispatch]);

  // Debounce the difficulty input to avoid too many dispatches
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedDifficulty(difficulty);
    }, 2000); // 300–500ms is a good range
    console.log("debouncedDifficulty", debouncedDifficulty);
    return () => {
      clearTimeout(handler);
    };
  }, [difficulty]);

  // Fetch snippet only when debounced difficulty changes
  useEffect(() => {
    if (typeof id === "string") {
      console.log("fetchSnippet", difficulty);
      dispatch(fetchSnippet(id, ifmask, debouncedDifficulty));
    }
  }, [debouncedDifficulty]);

  // Optional: on initial load (with current difficulty)
  useEffect(() => {
    if (typeof id === "string") {
      dispatch(fetchSnippet(id, ifmask, difficulty));
    }
  }, [id, dispatch]);

  useEffect(() => {
    if (snippet?.maskedContent) {
      const blanksCount = (snippet.maskedContent.match(/___/g) || []).length;
      setUserInputs(new Array(blanksCount).fill(""));
      setAnswerMatches(new Array(blanksCount).fill(false));
    }
  }, [snippet]);

  useEffect(() => {
    if (["success", "error", "not_found"].includes(status)) {
      const timer = setTimeout(() => {
        dispatch(setFetchSnippetStatus("idle"));
      }, 3000);

      return () => clearTimeout(timer); // cleanup in case the component unmounts or status changes early
    }
  }, [status, dispatch]);

  const handleChange = (index: number, value: string) => {
    const updatedInputs = [...userInputs];
    updatedInputs[index] = value;
    setUserInputs(updatedInputs);
  };

  const renderMaskedContentWithInputs = () => {
    if (!snippet?.maskedContent) {
      return null;
    }

    const parts = snippet.maskedContent.split("___");
    const blanksCount = parts.length - 1;

    return (
      <div className="bg-gray-900 text-white p-4 rounded whitespace-pre-wrap font-mono leading-loose">
        {parts.map((part: string, i: number) => (
          <React.Fragment key={`part-${i}`}>
            {part}
            {i < blanksCount && (
              <div className="relative inline-block text-center">
                <input
                  type="text"
                  value={userInputs[i] ?? ""}
                  onChange={(e) => handleChange(i, e.target.value)}
                  className={`bg-transparent border-b
                   ${
                     hasSubmitted
                       ? answerMatches[i]
                         ? "border-green-400 text-green-400"
                         : "border-red-500 text-red-500 animate-pulse"
                       : "border-gray-500 text-white"
                   }
                   w-20 mx-1 px-1 focus:outline-none focus:border-b-2
                   placeholder-gray-500 transition-all duration-150
                 `}
                  spellCheck={false}
                  autoComplete="off"
                />
                {hasSubmitted && !answerMatches[i] && (
                  <div className="absolute z-40 -bottom-6 left-1/2 -translate-x-1/2 text-xs text-red-400 bg-gray-900 px-2 py-0.5 rounded shadow-lg whitespace-nowrap">
                    Correct: {snippet.answer[i]}
                  </div>
                )}
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    );
  };

  const handleSubmit = () => {
    if (!snippet?.answer && !snippet?.language) {
      return;
    }
    if (!userInputs.some((input) => input.trim() !== "")) {
      alert("You have to fill at least one blank");
      return; // Stop the submission or scoring process here
    }

    const results = snippet.answer.map((correctAns: string, i: number) => {
      const userAns = userInputs[i] || "";
      const similarity = stringSimilarity.compareTwoStrings(
        userAns.trim(),
        correctAns.trim()
      );
      return {
        match: similarity >= threshold,
        similarity,
      };
    });

    const matches = results.map((r: Result) => r.match);
    const similarities = results.map((r: Result) => r.similarity);

    console.log("matches", matches);

    const averageSimilarity =
      similarities.reduce((sum: number, sim: number) => sum + sim, 0) /
      similarities.length;

    console.log("averageSimilarity", averageSimilarity);
    // Normalize difficulty if needed (assuming 1–10 scale)
    const normalizedDifficulty = Math.min(1, (difficulty || 1) / 10);
    console.log("threshold", threshold);
    console.log("difficulty", difficulty);

    // Compute weighted score: difficulty is weighted more heavily
    const score = Math.min(
      100,
      Math.round(
        Math.pow(averageSimilarity, 1.5) * 80 +
          Math.pow(normalizedDifficulty, 0.7) * 20
      )
    );
    console.log("score", score);

    setAnswerMatches(matches);
    setHasSubmitted(true);

    dispatch(
      addLeaderboardEntry({
        language: snippet?.language,
        score,
        userId: String(userDBData.id),
        userName: String(userDBData.username),
        similarity: averageSimilarity,
        difficulty: difficulty,
        snippetId: String(snippet.id),
        dateOfSubmission: new Date().toISOString(),
      })
    );
  };

  const handleResetAll = () => {
    if (snippet?.maskedContent) {
      const blanksCount = (snippet.maskedContent.match(/___/g) || []).length;
      setUserInputs(new Array(blanksCount).fill(""));
      setAnswerMatches(new Array(blanksCount).fill(false));
      setHasSubmitted(false);
      setDifficulty(5); // If you want to reset difficulty
    }
  };

  return (
    <div className="bg-[#000d2a] min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow p-6 max-w-4xl mx-auto text-white">
        <div className="flex flex-col items-center justify-between mb-6 w-full">
          {/* Title Row */}
          <div className="flex w-full items-center justify-between">
            <h1 className="text-3xl font-extrabold text-[#A0FF70] drop-shadow-lg text-center w-full">
              🧠 Solve the Snippet
            </h1>
            <button
              onClick={handleResetAll}
              className=" flex items-center gap-2 bg-gray-700 hover:bg-gray-600 text-white text-sm px-3 py-2 rounded-lg shadow-md"
              aria-label="Reset inputs and answers"
            >
              <span>🔁</span>
              <span>Reset</span>
            </button>
          </div>

          {/* Instructions */}
          <p className="text-gray-300 mt-3 text-sm text-center max-w-xl">
            Fill in the missing code above. Use the accuracy slider to control
            how exact your answer must be. Click{" "}
            <span className="text-[#A0FF70] font-medium">Submit</span> to check
            your solution.
          </p>
        </div>

        {status !== "idle" && (
          <div className="mb-4 rounded text-sm font-medium">
            {status === "loading" && (
              <p className="text-yellow-300 bg-yellow-800 bg-opacity-20 px-3 py-2 rounded">
                ⏳ Loading snippet...
              </p>
            )}
            {status === "success" && (
              <p className="text-green-300 bg-green-800 bg-opacity-20 px-3 py-2 rounded">
                ✅ Snippet loaded successfully!
              </p>
            )}
            {status === "error" && (
              <p className="text-red-300 bg-red-800 bg-opacity-20 px-3 py-2 rounded">
                ❌ Failed to load snippet. Please try again.
              </p>
            )}
            {status === "not_found" && (
              <p className="text-gray-300 bg-gray-700 bg-opacity-20 px-3 py-2 rounded">
                ⚠️ Snippet not found.
              </p>
            )}
          </div>
        )}

        <section className="mb-8 bg-gradient-to-br from-indigo-900 via-[#001848] to-[#000a32] p-6 rounded-2xl shadow-lg border border-indigo-700">
          <h2 className="text-2xl font-semibold mb-4 tracking-tight text-indigo-200 drop-shadow-sm">
            {snippet?.title || "Snippet Title"}
          </h2>

          <div className="bg-[#001b55] p-6 rounded-xl font-mono text-white whitespace-pre-wrap leading-relaxed shadow-inner border border-indigo-600">
            {renderMaskedContentWithInputs()}
          </div>
        </section>

        <div className="flex flex-row items-center justify-between bg-gradient-to-br from-indigo-900 via-[#001848] to-[#000a32] rounded-xl p-6 shadow-lg space-x-8 mb-6">
          {/* Submit Button */}
          <button
            className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-2 rounded-xl shadow-md transition-all duration-200"
            onClick={handleSubmit}
          >
            Submit
          </button>

          {/* Difficulty Slider */}
          <div className="flex flex-col items-center space-y-2">
            <label
              htmlFor="difficulty"
              className="text-white text-sm font-medium"
            >
              Difficulty
            </label>
            <input
              id="difficulty"
              type="range"
              min={1}
              max={10}
              value={difficulty}
              onChange={(e) => setDifficulty(parseInt(e.target.value))}
              className="w-40 accent-purple-800"
            />
            <span className="text-purple-500 font-semibold">
              {(difficulty * 10).toFixed(0)}%
            </span>
          </div>

          {/* Similarity Threshold Slider */}
          <div className="flex flex-col items-center space-y-2">
            <label
              htmlFor="threshold"
              className="text-white text-sm font-medium"
            >
              Accuracy Sensitivity
            </label>
            <input
              id="threshold"
              type="range"
              min={1}
              max={10}
              value={threshold * 10}
              onChange={(e) => setThreshold(parseInt(e.target.value) / 10)}
              className="w-40 accent-blue-800"
            />
            <span className="text-blue-500 font-semibold">
              {(threshold * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default SolvePage;
