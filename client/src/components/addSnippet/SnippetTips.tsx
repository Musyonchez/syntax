import React from "react";

const SnippetTips = () => (
  <div className="mt-12 bg-gray-800 p-6 rounded-lg">
    <h2 className="text-xl font-semibold mb-3">💡 Tips for Practicing</h2>
    <ul className="list-disc list-inside space-y-2 text-gray-300">
      <li>After saving, go to the <strong>/practice</strong> page to fill in the blanks.</li>
      <li>Short functions (5–15 lines) work best for focused learning.</li>
      <li>Practice common patterns like loops, conditionals, and built-ins.</li>
      <li>Try writing reusable code like utility functions or common API handlers.</li>
      <li>Use the Practice page regularly to sharpen your memory and fluency.</li>
    </ul>
  </div>
);

export default SnippetTips;
