import React from "react";

type Props = {
  status: string;
};

const SnippetSuccessError: React.FC<Props> = ({ status }) => {
  if (status === "loading") {
    return <p className="mt-4 text-yellow-400 animate-pulse">⏳ Saving snippet...</p>;
  }

  if (status === "success") {
    return <p className="mt-4 text-green-400">✅ Snippet added successfully!</p>;
  }

  if (status === "error") {
    return <p className="mt-4 text-red-400">❌ Failed to add snippet. Try again.</p>;
  }

  return null;
};

export default SnippetSuccessError;
