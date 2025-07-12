import React from "react";
import { Snippet } from "@/types";

interface Props {
  snippet: Snippet;
  onToggleFavorite: (id: string) => void;
}

const SnippetCard: React.FC<Props> = ({ snippet, onToggleFavorite }) => {
  return (
    <div
      className="relative border p-4 rounded shadow hover:shadow-lg transition cursor-pointer"
      onClick={() => window.open(`/solve/${snippet.id}`, "_blank")}
    >
      <div
        className={`absolute top-1 right-4 ${
          snippet.favorite ? "text-red-500" : "text-gray-400"
        } hover:text-red-600`}
        onClick={(e) => {
          e.stopPropagation();
          onToggleFavorite(snippet.id);
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill={snippet.favorite ? "currentColor" : "none"}
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z"
          />
        </svg>
      </div>

      <h3 className="font-semibold text-lg mb-2 truncate">{snippet.title}</h3>

      <pre className="bg-gray-100 p-2 rounded overflow-x-auto text-sm text-black">
        {snippet.content?.split("\n").slice(0, 10).join("\n") || ""}
      </pre>
    </div>
  );
};

export default SnippetCard;
