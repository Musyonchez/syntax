import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/store";
import {
  fetchSnippet,
  setFetchSnippetStatus,
} from "@/store/snippet_store/actions";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

//pulse to encourage hover

const SolvePage: React.FC = () => {
  const router = useRouter();
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

  // Debounce the difficulty input to avoid too many dispatches
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedDifficulty(difficulty);
    }, 2000); // 300–500ms is a good range

    return () => {
      clearTimeout(handler);
    };
  }, [difficulty]);

  // Fetch snippet only when debounced difficulty changes
  useEffect(() => {
    if (typeof id === "string") {
      dispatch(fetchSnippet(id, true, debouncedDifficulty));
    }
  }, [debouncedDifficulty]);

  // Optional: on initial load (with current difficulty)
  useEffect(() => {
    if (typeof id === "string") {
      dispatch(fetchSnippet(id, true, difficulty));
    }
  }, [id, true, dispatch]);

  useEffect(() => {
    if (snippet?.maskedContent) {
      const blanksCount = (snippet.maskedContent.match(/___/g) || []).length;
      setUserInputs(new Array(blanksCount).fill(""));
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

    // Example: Replace ___ with input boxes
    let parts = snippet.maskedContent.split("___");
    return (
      <pre className="bg-gray-900 text-white p-4 rounded whitespace-pre-wrap leading-loose">
        {parts.map((part: string, i: number) => (
          <React.Fragment key={i}>
            {part}
            {i < userInputs.length && (
              <input
                type="text"
                value={userInputs[i]}
                onChange={(e) => handleChange(i, e.target.value)}
                className="bg-transparent border-b border-gray-500 text-white w-20 mx-1 px-1 focus:outline-none focus:border-b-2 focus:border-blue-400 placeholder-gray-500 transition-all duration-150"
              />
            )}
          </React.Fragment>
        ))}
      </pre>
    );
  };

  return (
    <div className="bg-[#000d2a] min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow p-6 max-w-4xl mx-auto text-white">
        <h1 className="text-2xl font-bold mb-4">Solve Snippet</h1>
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
          className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          onClick={() => {
            // Will implement validation next
            console.log("User submission:", userInputs);
          }}
        >
          Submit
        </button>

        {/* Difficulty slider and current value */}
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
