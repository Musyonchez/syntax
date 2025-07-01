import React, { useEffect, useState, useRef } from "react";
import { useRouter } from "next/router";
import { useDispatch, useSelector } from "react-redux";
import stringSimilarity from "string-similarity";
import { RootState } from "@/store";
import {
  fetchSnippet,
  setFetchSnippetStatus,
} from "@/store/snippet_store/actions";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const SolvePage: React.FC = () => {
  const router = useRouter();
  const dispatch = useDispatch();
  const { id } = router.query;

  const snippet = useSelector((state: RootState) => state.snippet.snippet);
  const status = useSelector(
    (state: RootState) => state.snippet.fetchSnippetStatus,
  );

  const [userInputs, setUserInputs] = useState<string[]>([]);
  const [answerMatches, setAnswerMatches] = useState<boolean[]>([]); // true/false per answer
  const [difficulty, setDifficulty] = useState<number>(5);
  const [debouncedDifficulty, setDebouncedDifficulty] =
    useState<number>(difficulty);

  // Reference for scrolling
  const topRef = useRef<HTMLDivElement>(null);

  // Debounce difficulty input
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedDifficulty(difficulty);
    }, 400);

    return () => {
      clearTimeout(handler);
    };
  }, [difficulty]);

  // Fetch snippet on id or debounced difficulty change
  useEffect(() => {
    if (typeof id === "string") {
      dispatch(fetchSnippet(id, true, debouncedDifficulty));
      resetAll(); // Reset inputs and matches when snippet changes
    }
  }, [id, debouncedDifficulty]);

  // Setup user inputs array on snippet load
  useEffect(() => {
    if (snippet?.maskedContent) {
      const blanksCount = (snippet.maskedContent.match(/___/g) || []).length;
      setUserInputs(new Array(blanksCount).fill(""));
      setAnswerMatches(new Array(blanksCount).fill(false));
    }
  }, [snippet]);

  // Reset everything
  const resetAll = () => {
    if (snippet?.maskedContent) {
      const blanksCount = (snippet.maskedContent.match(/___/g) || []).length;
      setUserInputs(new Array(blanksCount).fill(""));
      setAnswerMatches(new Array(blanksCount).fill(false));
    }
  };

  // Handle user input change
  const handleChange = (index: number, value: string) => {
    const updatedInputs = [...userInputs];
    updatedInputs[index] = value;
    setUserInputs(updatedInputs);
  };

  // Submit handler - compare answers with string similarity
  const handleSubmit = () => {
    if (!snippet?.answer) {
      return;
    }

    const threshold = 0.8; // similarity threshold for match (adjust as needed)
    const matches = snippet.answer.map((correctAns: string, i: number) => {
      const userAns = userInputs[i] || "";
      const similarity = stringSimilarity.compareTwoStrings(
        userAns.trim().toLowerCase(),
        correctAns.trim().toLowerCase(),
      );
      return similarity >= threshold;
    });

    setAnswerMatches(matches);

    // Scroll to top after submit
    topRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Render masked content with inputs and highlighting + tooltip on incorrect
  const renderMaskedContentWithInputs = () => {
    if (!snippet?.maskedContent) {
      return null;
    }

    const parts = snippet.maskedContent.split("___");

    return (
      <pre className="bg-gray-900 text-white p-4 rounded whitespace-pre-wrap leading-loose">
        {parts.map((part: string, i: number) => (
          <React.Fragment key={i}>
            {part}
            {i < userInputs.length && (
              <Tooltip
                content={answerMatches[i] ? "" : snippet.answer[i]}
                visible={!answerMatches[i]}
              >
                <input
                  type="text"
                  value={userInputs[i]}
                  onChange={(e) => handleChange(i, e.target.value)}
                  className={`bg-transparent border-b 
                    ${
                      answerMatches[i]
                        ? "border-green-400 text-green-400"
                        : "border-red-500 text-red-500 animate-pulse"
                    }
                    w-20 mx-1 px-1 focus:outline-none focus:border-b-2
                    placeholder-gray-500 transition-all duration-150
                  `}
                  spellCheck={false}
                />
              </Tooltip>
            )}
          </React.Fragment>
        ))}
      </pre>
    );
  };

  // Tooltip component for hover box
  const Tooltip: React.FC<{
    content: string;
    visible: boolean;
    children: React.ReactNode;
  }> = ({ content, visible, children }) => {
    return (
      <span className="relative group inline-block">
        {children}
        {visible && (
          <div
            className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2
            w-max max-w-xs bg-gray-800 text-white text-xs rounded px-2 py-1
            opacity-0 group-hover:opacity-100 transition-opacity duration-300
            pointer-events-none z-10
            whitespace-normal break-words
            shadow-lg"
          >
            {content}
          </div>
        )}
      </span>
    );
  };

  return (
    <div className="bg-[#000d2a] min-h-screen flex flex-col" ref={topRef}>
      <Navbar />
      <main className="flex-grow p-6 max-w-4xl mx-auto text-white">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold">Solve Snippet</h1>
          <button
            onClick={resetAll}
            className="bg-gray-700 hover:bg-gray-600 text-white text-sm px-4 py-1 rounded transition"
            aria-label="Reset inputs and answers"
          >
            Reset
          </button>
        </div>

        {status !== "idle" && (
          <div className="mb-4 p-3 rounded text-sm font-medium">
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

        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">{snippet?.title}</h2>
          {renderMaskedContentWithInputs()}
        </div>

        <button
          className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 mb-6"
          onClick={handleSubmit}
        >
          Submit
        </button>

        {/* Difficulty slider */}
        <div className="flex items-center space-x-4 mb-4">
          <label htmlFor="difficulty" className="text-white font-medium">
            Difficulty:
          </label>
          <input
            id="difficulty"
            type="range"
            min={1}
            max={10}
            value={difficulty}
            onChange={(e) => setDifficulty(parseInt(e.target.value))}
            className="w-48"
          />
          <span className="text-white font-semibold">{difficulty}</span>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default SolvePage;
