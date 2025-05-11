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

// import React, { useEffect } from "react";
// import { useSelector, useDispatch } from "react-redux";
// import { fetchSnippets, addSnippet } from "../store/users_store/actions";

// const SnippetList = () => {
//   const dispatch = useDispatch();

//   // Access snippets from Redux store
//   const snippets = useSelector((state: any) => state.snippets);

//   useEffect(() => {
//     // Dispatch action to fetch snippets on component mount
//     dispatch(fetchSnippets());
//   }, [dispatch]);

//   return (
//     <div>
//       {snippets.map((snippet: any) => (
//         <div key={snippet.id}>
//           <h3>{snippet.title}</h3>
//           <pre>{snippet.content}</pre>
//         </div>
//       ))}
//     </div>
//   );
// };

// export default SnippetList;




import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchUsers, addUser } from "../store/user_store/actions";
import { RootState } from "../store/";

const UserList = () => {
  const dispatch = useDispatch();

  const users = useSelector((state: RootState) => state.user.users);
  const status = useSelector((state: RootState) => state.user.addUserStatus);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  const handleAddUser = () => {
    const newUser = {
      username: "testuser",
      email: "test@example.com",
      password: "jdfhslfsdh",
      createdAt: new Date().toISOString(),
    };
    dispatch(addUser(newUser));
  };

  return (
    <div>
      <h2>User List</h2>

      {status === "loading" && <p>Loading users...</p>}
      {status === "error" && (
        <p style={{ color: "red" }}>Failed to add user. Please try again.</p>
      )}
      {status === "success" && (
        <p style={{ color: "green" }}>User added successfully!</p>
      )}

      {users && users.length > 0 ? (
        users.map((user: any) => (
          <div key={user.id} style={{ marginBottom: "1rem" }}>
            <h3>{user.username}</h3>
            <p>{user.email}</p>
          </div>
        ))
      ) : (
        <p>No users found.</p>
      )}

      <button onClick={handleAddUser}>Add Test User</button>
    </div>
  );
};

export default UserList;
