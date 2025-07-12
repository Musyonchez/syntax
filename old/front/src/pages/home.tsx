import React, { useState } from "react";

const Home = () => {
  const [code, setCode] = useState("print('Sum of the array is', sum)");
  const handleFormat = async () => {
    const response = await fetch("/api/format", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code, language: "python" }),
    });

    const data = await response.json();
    setCode(data.formatted);
  };
  return (
    <div className=" min-h-screen bg-white text-black p-24 flex flex-col">
      <textarea
        className=" h-36 w-96 p-5 border-2 border-black rounded-lg"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      ></textarea>
      <button onClick={handleFormat}>Format</button>
    </div>
  );
};

export default Home;
