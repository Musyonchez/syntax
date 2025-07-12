import { useState } from "react";

export default function Home() {
  const [ast, setAst] = useState(null);
  const [code, setCode] = useState("print('Sum of the array is ', ans)");

  const analyzeCode = async () => {
    const selection = window.getSelection();
    let highlightedCode = "";

    if (selection) {
      highlightedCode = selection.toString();
    } else {
      alert("No code is selected");
      return;
    }

    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: highlightedCode, language: "python" }),
    });

    const data = await response.json();
    setAst(data.ast);
  };

  const [exercise, setExercise] = useState("");
  const [answer, setAnswer] = useState("");

  const generateExercise = async () => {
    const response = await fetch("/api/generate-exercise", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ast: ast }),
    });

    const data = await response.json();
    setExercise(data.exercise);
  };

  const checkAnswer = () => {
    // Logic to compare user input with the original AST
  };

  return (
    <>
      <div>
        <button onClick={generateExercise}>Generate Exercise</button>
        {exercise && (
          <div>
            <pre>{exercise}</pre>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Fill in the blanks"
            />
            <button onClick={checkAnswer}>Check Answer</button>
          </div>
        )}
      </div>

      <div className=" text-black min-h-screen bg-blue-600">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{ width: "100%", height: "250px" }}
        />
        <button onClick={analyzeCode}>Analyze Highlighted Code</button>

        {ast && <pre>{JSON.stringify(ast, null, 2)}</pre>}
      </div>
    </>
  );
}
