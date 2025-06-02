import React from "react";
import { Snippet } from "@/types";

interface Props {
  snippet: Snippet;
  onToggleFavorite: (id: string) => void;
  onToggleDelete: (id: string) => void;
}

const SnippetCard: React.FC<Props> = ({
  snippet,
  onToggleFavorite,
  onToggleDelete,
}) => {
  return (
    <div
      className="relative border p-4 rounded shadow hover:shadow-lg transition cursor-pointer"
      onClick={() => window.open(`/solve/${snippet.id}`, "_blank")}
    >
      <div
        className={`absolute top-1 right-9 ${
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

      <div
        className={`absolute top-1 right-2 hover:text-red-600`}
        onClick={(e) => {
          e.stopPropagation();
          onToggleDelete(snippet.id);
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
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
