export default async function analyzeCode(code: string, language: string) {
  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code, language }),
  });
  // const text = await response.text();
  // console.log("Raw response:", text); // Log the raw response for debugging
  try {
    const data = await response.json();
    console.log(data.ast);
  } catch (error) {
    console.error("Failed to parse JSON:", error);
  }
}
