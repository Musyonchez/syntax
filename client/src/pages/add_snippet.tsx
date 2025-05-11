import React, { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useDispatch, useSelector } from "react-redux";
import { addSnippet, setAddSnippetStatus } from "../store/actions";
import { RootState } from "../store";

const AddSnippet = () => {
  const dispatch = useDispatch();
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [language, setLanguage] = useState("python");
  const status = useSelector((state: RootState) => state.addSnippetStatus);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !content || !language) {
      return;
    }

    dispatch(
      addSnippet({
        title,
        content,
        language,
        createdAt: new Date().toISOString(),
        userId: 1,
      })
    );
  };

  // Reset form and status on success
  useEffect(() => {
    if (status === "success") {
      setTitle("");
      setContent("");
      setLanguage("python");

      setTimeout(() => {
        dispatch(setAddSnippetStatus("idle"));
      }, 3000);
    }
  }, [status]);

  return (
    <>
      <Navbar />
      <div className="flex flex-col min-h-screen bg-[#000d2a] text-white">
        <main className="flex-grow py-10 px-6 max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-4 text-center text-[#A0FF70]">
            Add a Code Snippet
          </h1>
          <p className="text-center mb-10 text-[#A0FF70]">
            Welcome to the Quiz Builder! Paste in your code, choose a language,
            and give it a name. We’ll turn it into a syntax quiz for you to
            master.
          </p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block mb-1 font-medium">Snippet Name:</label>
              <input
                type="text"
                placeholder="e.g. Add Two Numbers"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="block w-full border border-gray-300 rounded-md p-3 font-mono text-white bg-gray-900"
              />
              <p className="text-sm text-gray-400 mt-1">
                Give your snippet a short title like “Addition Function.”
              </p>
            </div>

            <div>
              <label htmlFor="language" className="block mb-1 font-medium">
                Choose Language:
              </label>
              <select
                id="language"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full border border-gray-300 rounded-md p-2 text-white bg-gray-900"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
              </select>
              <p className="text-sm text-gray-400 mt-1">
                Currently supporting Python and JavaScript.
              </p>
            </div>

            <div>
              <label htmlFor="code" className="block mb-1 font-medium">
                Paste Your Code:
              </label>
              <textarea
                id="code"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                rows={10}
                className="w-full border border-gray-300 rounded-md p-3 font-mono text-white bg-gray-900"
                placeholder={`# Simple addition
def add(a, b):
    return a + b`}
              />
              <p className="text-sm text-gray-400 mt-1">
                We’ll mask parts of this to help you practice recalling syntax.
              </p>
            </div>

            <button
              type="submit"
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
              disabled={status === "loading"}
            >
              {status === "loading" ? "Saving..." : "Save Snippet"}
            </button>
            {status === "success" && (
              <p className="mt-4 text-green-400">
                ✅ Snippet added successfully!
              </p>
            )}
            {status === "error" && (
              <p className="mt-4 text-red-400">
                ❌ Failed to add snippet. Try again.
              </p>
            )}
          </form>

          <div className="mt-12 bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-3">
              💡 Tips for Practicing
            </h2>
            <ul className="list-disc list-inside space-y-2 text-gray-300">
              <li>
                After saving, go to the <strong>/practice</strong> page to fill
                in the blanks.
              </li>
              <li>
                Short functions (5–15 lines) work best for focused learning.
              </li>
              <li>
                Practice common patterns like loops, conditionals, and
                built-ins.
              </li>
              <li>
                Try writing reusable code like utility functions or common API
                handlers.
              </li>
              <li>
                Use the Practice page regularly to sharpen your memory and
                fluency.
              </li>
            </ul>
          </div>
        </main>
      </div>
      <Footer />
    </>
  );
};

export default AddSnippet;

// import React, { useState } from "react";
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";

// const Quiz = () => {
//   const [content, setContent] = useState("");
//   const [title, setTitle] = useState("");
//   const [language, setLanguage] = useState("python");

//   const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
//     e.preventDefault();
//     // 🔧 Handle backend submission
//     console.log("Submitted content:", content);
//     console.log("Submitted title:", title);
//     console.log("Selected language:", language);
//   };

//   return (
//     <>
//       <Navbar />
//       <div className="flex flex-col min-h-screen bg-[#000d2a] text-white">
//         <main className="flex-grow py-10 px-6 max-w-4xl mx-auto">
//           <h1 className="text-3xl font-bold mb-4 text-center text-[#A0FF70]">
//             Add a Code Snippet
//           </h1>
//           <p className="text-center mb-10 text-[#A0FF70]">
//             Welcome to the Quiz Builder! Paste in your code, choose a language,
//             and give it a name. We’ll turn it into a syntax quiz for you to
//             master.
//           </p>

//           <form onSubmit={handleSubmit} className="space-y-6">
//             {/* Name of snippet */}
//             <div>
//               <label className="block mb-1 font-medium">Snippet Name:</label>
//               <input
//                 type="text"
//                 placeholder="e.g. Add Two Numbers"
//                 value={title}
//                 onChange={(e) => setTitle(e.target.value)}
//                 className="block w-full border border-gray-300 rounded-md p-3 font-mono text-white bg-gray-900"
//               />
//               <p className="text-sm text-gray-400 mt-1">
//                 Give your snippet a short title like “Addition Function.”
//               </p>
//             </div>

//             {/* Language Selector */}
//             <div>
//               <label htmlFor="language" className="block mb-1 font-medium">
//                 Choose Language:
//               </label>
//               <select
//                 id="language"
//                 value={language}
//                 onChange={(e) => setLanguage(e.target.value)}
//                 className="w-full border border-gray-300 rounded-md p-2 text-white bg-gray-900"
//               >
//                 <option value="python">Python</option>
//                 <option value="javascript">JavaScript</option>
//               </select>
//               <p className="text-sm text-gray-400 mt-1">
//                 Currently supporting Python and JavaScript.
//               </p>
//             </div>

//             {/* Code Textarea */}
//             <div>
//               <label htmlFor="code" className="block mb-1 font-medium">
//                 Paste Your Code:
//               </label>
//               <textarea
//                 id="code"
//                 value={content}
//                 onChange={(e) => setContent(e.target.value)}
//                 rows={10}
//                 className="w-full border border-gray-300 rounded-md p-3 font-mono text-white bg-gray-900"
//                 placeholder={`For Example Can Be Either Of:

// # Simple addition
//     def add(a, b):
//       return a + b

// # ----------------------------

// # Advanced: add multiple numbers
//     def add_numbers(*args):
//         total = 0
//         for num in args:
//             if isinstance(num, (int, float)):
//                 total += num
//         return total`}
//               />

//               <p className="text-sm text-gray-400 mt-1">
//                 We’ll mask parts of this to help you practice recalling syntax.
//               </p>
//             </div>

//             {/* Submit Button */}
//             <button
//               type="submit"
//               className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
//             >
//               Save Snippet
//             </button>
//           </form>

//           {/* Guide Section */}
//           <div className="mt-12 bg-gray-800 p-6 rounded-lg">
//             <h2 className="text-xl font-semibold mb-3">
//               💡 Tips for Practicing
//             </h2>
//             <ul className="list-disc list-inside space-y-2 text-gray-300">
//               <li>
//                 After saving, go to the <strong>/practice</strong> page to fill
//                 in the blanks.
//               </li>
//               <li>
//                 Short functions (5–15 lines) work best for focused learning.
//               </li>
//               <li>
//                 Practice common patterns like loops, conditionals, and
//                 built-ins.
//               </li>
//               <li>
//                 Try writing reusable code like utility functions or common API
//                 handlers.
//               </li>
//               <li>
//                 Use the Practice page regularly to sharpen your memory and
//                 fluency.
//               </li>
//             </ul>
//           </div>
//         </main>
//       </div>
//       <Footer />
//     </>
//   );
// };

// export default Quiz;
