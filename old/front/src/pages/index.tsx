import React, { useState } from "react";
import analyzeCode from "../utils/analyzeCode";

const Index: React.FC = () => {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    analyzeCode(text, "python");
    console.log("Submitted Text:", text);
    // Add your form submission logic here
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-indigo-400 to-purple-600">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          Submit Your Text
        </h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="textarea"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Enter your text
            </label>
            <textarea
              id="textarea"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full h-40 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 resize-none"
              placeholder="Write something here..."
            />
          </div>
          <div>
            <button
              type="submit"
              className="w-full py-3 bg-indigo-500 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-300 ease-in-out"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Index;
