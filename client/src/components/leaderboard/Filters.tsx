// components/leaderboard/Filters.tsx
import React from "react";

interface FiltersProps {
  selectedTime: string;
  selectedLanguage: string;
  setSelectedTime: (val: string) => void;
  setSelectedLanguage: (val: string) => void;
  validTimes: string[];
  validLanguages: string[];
}

export default function LeaderboardFilters({
  selectedTime,
  selectedLanguage,
  setSelectedTime,
  setSelectedLanguage,
  validTimes,
  validLanguages,
}: FiltersProps) {
  return (
    <div className="flex flex-wrap gap-4 mb-8 justify-center">
      <div className="flex flex-col">
        <label htmlFor="time" className="text-sm text-gray-300 mb-1">Time Period</label>
        <select
          id="time"
          value={selectedTime}
          onChange={(e) => setSelectedTime(e.target.value)}
          className="bg-[#0a1b44] text-white border border-[#A0FF70] rounded-xl px-4 py-2 hover:border-white focus:outline-none focus:ring focus:ring-[#A0FF70]"
        >
          {validTimes.map((time) => (
            <option key={time} value={time}>
              {time.charAt(0).toUpperCase() + time.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col">
        <label htmlFor="language" className="text-sm text-gray-300 mb-1">Language</label>
        <select
          id="language"
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          className="bg-[#0a1b44] text-white border border-[#A0FF70] rounded-xl px-4 py-2 hover:border-white focus:outline-none focus:ring focus:ring-[#A0FF70]"
        >
          {validLanguages.map((lang) => (
            <option key={lang} value={lang}>
              {lang.charAt(0).toUpperCase() + lang.slice(1)}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
