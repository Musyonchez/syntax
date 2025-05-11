// import React, { useState } from "react";
// import { useDispatch } from "react-redux";
// import { addSnippet } from "../store/actions";
// import Navbar from "@/components/Navbar";

// const AddSnippetForm = () => {
//   const dispatch = useDispatch();
//   const [title, setTitle] = useState("");
//   const [content, setContent] = useState("");

//   const handleSubmit = (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!title || !content) return;

//     dispatch(addSnippet({ title, content }));

//     // Clear inputs
//     setTitle("");
//     setContent("");
//   };

//   return (
//     <>
//       <Navbar />
//       <form onSubmit={handleSubmit}>
//         <h2>Add New Snippet</h2>
//         <div>
//           <label>Title:</label>
//           <input
//             type="text"
//             value={title}
//             onChange={(e) => setTitle(e.target.value)}
//           />
//         </div>
//         <div>
//           <label>Content:</label>
//           <textarea
//             rows={5}
//             value={content}
//             onChange={(e) => setContent(e.target.value)}
//           />
//         </div>
//         <button type="submit">Add Snippet</button>
//       </form>
//     </>
//   );
// };

// export default AddSnippetForm;

import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchSnippets, addSnippet } from "../store/actions";

const SnippetList = () => {
  const dispatch = useDispatch();

  // Access snippets from Redux store
  const snippets = useSelector((state: any) => state.snippets);

  useEffect(() => {
    // Dispatch action to fetch snippets on component mount
    dispatch(fetchSnippets());
  }, [dispatch]);

  return (
    <div>
      {snippets.map((snippet: any) => (
        <div key={snippet.id}>
          <h3>{snippet.title}</h3>
          <pre>{snippet.content}</pre>
        </div>
      ))}
    </div>
  );
};

export default SnippetList;
