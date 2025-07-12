import React from "react";

const MainContent = () => {
  return (
    <div className="mt-10 mx-auto w-[1200px] border-2 border-gray-600 rounded-[2rem] min-h-[80vh] p-6">
      <div className="w-full flex justify-around items-center mb-6 gap-4 flex-wrap">
        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Submit</button>
        <button className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">Refresh</button>
       <div className=" flex items-center">
       <label htmlFor="language" className="text-lg font-semibold mr-3">Choose a language:</label>
        <select
          name="language"
          id="language"
          className="border border-gray-400 rounded px-3 py-2"
        >
          <option value="Java">Java</option>
          <option value="JavaScript">JavaScript</option>
          <option value="Python">Python</option>
          <option value="C#">C#</option>
        </select>
       </div>
      </div>

      <textarea
        name="mainTextarea"
        id="mainTextarea"
        placeholder="Type something here..."
        className="w-full min-h-[60vh] p-4 border border-gray-400 rounded-lg resize-none"
      ></textarea>
    </div>
  );
};

export default MainContent;
