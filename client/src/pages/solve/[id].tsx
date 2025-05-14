import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/store";
import { fetchSnippet, setFetchSnippetStatus } from "@/store/snippet_store/actions";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const SolvePage: React.FC = () => {
  const router = useRouter();
  const dispatch = useDispatch();
  const { id } = router.query;

  const snippet = useSelector((state: RootState) => state.snippet.snippet);
  const status = useSelector(
    (state: RootState) => state.snippet.fetchSnippetStatus
  );
  const [userInputs, setUserInputs] = useState<string[]>([]);

  useEffect(() => {
    if (typeof id === "string") {
      dispatch(fetchSnippet(id as string));
    }
  }, [id, dispatch]);

  useEffect(() => {
    if (snippet?.content) {
      const blanksCount = (snippet.content.match(/___/g) || []).length;
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

  const renderContentWithInputs = () => {
    if (!snippet?.content) return null;

    // Example: Replace ___ with input boxes
    let parts = snippet.content.split("___");
    return (
      <pre className="bg-black text-white p-4 rounded whitespace-pre-wrap leading-loose">
        {parts.map((part, i) => (
          <React.Fragment key={i}>
            {part}
            {i < userInputs.length && (
              <input
                type="text"
                value={userInputs[i]}
                onChange={(e) => handleChange(i, e.target.value)}
                className="inline-block w-20 mx-1 px-1 rounded border border-gray-400 text-black"
              />
            )}
          </React.Fragment>
        ))}
      </pre>
    );
  };

  console.log("snippet from sole/id", snippet);

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
          {renderContentWithInputs()}
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
      </main>
      <p className="mt-2 text-sm text-gray-400">Status: {status}</p>

      {status === "success" && (
        <p className="mt-4 text-green-400">✅ Snippet added successfully!</p>
      )}
      {status === "error" && (
        <p className="mt-4 text-red-400">
          ❌ Failed to add snippet. Try again.
        </p>
      )}
      <Footer />
    </div>
  );
};

export default SolvePage;
