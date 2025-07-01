import React from "react";

interface RandomButtonsProps {
  onOpenRandom: (type: "all" | "favorites" | "frequent") => void;
}

const RandomButtons: React.FC<RandomButtonsProps> = ({ onOpenRandom }) => {
  return (
    <div className=" md:ml-auto flex gap-2">
      <button
        onClick={() => onOpenRandom("all")}
        className="bg-gray-700 text-white px-3 py-1 rounded"
      >
        🎲 Random
      </button>
      <button
        onClick={() => onOpenRandom("favorites")}
        className="bg-yellow-600 text-white px-3 py-1 rounded"
      >
        ⭐ Favorites
      </button>
      <button
        onClick={() => onOpenRandom("frequent")}
        className="bg-purple-600 text-white px-3 py-1 rounded"
      >
        🔁 Frequent
      </button>
    </div>
  );
};

export default RandomButtons;
