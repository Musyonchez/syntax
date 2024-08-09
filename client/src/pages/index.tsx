import React from "react";
import analyzeCode from "../utils/analyzeCode";

const index = () => {
  const handleClick = () => {
    analyzeCode('print("Hello, world!")', "python");
  };
  return (
    <div>
      <h1>index</h1>
      <button onClick={handleClick}>Click</button>
    </div>
  );
};

export default index;
