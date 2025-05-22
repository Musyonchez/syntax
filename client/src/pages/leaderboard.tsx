import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/store";
import {
  fetchLeaderboard,
  setFetchLeaderboardStatus,
} from "@/store/leaderboard_store/actions";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const VALID_LANGUAGES = ["Python", "Javascript"];
const VALID_TIME_CATEGORIES = [
  "daily",
  "weekly",
  "monthly",
  "half-yearly",
  "yearly",
  "all-time",
];

const medalEmoji = (index: number) => {
  switch (index) {
    case 0:
      return "🥇";
    case 1:
      return "🥈";
    case 2:
      return "🥉";
    default:
      return `#${index + 1}`;
  }
};

export default function LeaderboardPage() {
  const dispatch = useDispatch();
  const { leaderboard, fetchLeaderboardStatus } = useSelector(
    (state: RootState) => state.leaderboard
  );

  const [selectedTime, setSelectedTime] = useState("daily");
  const [selectedLanguage, setSelectedLanguage] = useState("Python");

  const leaderboardKey = `${selectedTime}_${selectedLanguage}`;
  const categoryData = leaderboard[leaderboardKey];
  const entries = categoryData?.entries || [];

  useEffect(() => {
    dispatch(setFetchLeaderboardStatus("idle"));
    dispatch(fetchLeaderboard(leaderboardKey));
  }, [leaderboardKey, dispatch]);

  return (
    <div className="flex flex-col min-h-screen bg-[#000d2a] text-white">
      <Navbar />

      <main className="flex-1 px-4 py-8 max-w-4xl mx-auto w-full">
        <h1 className="text-4xl font-extrabold mb-6 text-[#A0FF70] text-center">
          🏆 Leaderboard 🏆
        </h1>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-8 justify-center">
          <div className="flex flex-col">
            <label htmlFor="time" className="text-sm text-gray-300 mb-1">
              Time Period
            </label>
            <select
              id="time"
              value={selectedTime}
              onChange={(e) => setSelectedTime(e.target.value)}
              className="bg-[#0a1b44] text-white border border-[#A0FF70] rounded-xl px-4 py-2 transition duration-200 hover:border-white focus:outline-none focus:ring focus:ring-[#A0FF70]"
            >
              {VALID_TIME_CATEGORIES.map((time) => (
                <option key={time} value={time}>
                  {time.charAt(0).toUpperCase() + time.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-col">
            <label htmlFor="language" className="text-sm text-gray-300 mb-1">
              Language
            </label>
            <select
              id="language"
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="bg-[#0a1b44] text-white border border-[#A0FF70] rounded-xl px-4 py-2 transition duration-200 hover:border-white focus:outline-none focus:ring focus:ring-[#A0FF70]"
            >
              {VALID_LANGUAGES.map((lang) => (
                <option key={lang} value={lang}>
                  {lang.charAt(0).toUpperCase() + lang.slice(1)}
                </option>
              ))}
            </select>
          </div>
        </div>

        <p className="mb-6 text-gray-300 text-center text-lg">
            Current Category:{" "}
            <span className="text-white font-semibold">
              🏆 {selectedTime.charAt(0).toUpperCase() + selectedTime.slice(1)}{" "}
              {selectedLanguage.charAt(0).toUpperCase() +
                selectedLanguage.slice(1)}
            </span>
        </p>

        {/* Status messages */}
        {fetchLeaderboardStatus === "loading" && (
          <p className="text-gray-400 text-center">⏳ Loading leaderboard...</p>
        )}
        {fetchLeaderboardStatus === "error" && (
          <p className="text-red-400 text-center">
            ❌ Failed to fetch leaderboard. Please try again later.
          </p>
        )}
        {fetchLeaderboardStatus === "not_found" && (
          <p className="text-yellow-400 text-center">
            ⚠️ No leaderboard data found for this category.
          </p>
        )}

        {/* Leaderboard entries */}
        {entries.length > 0 && (
          <ul className="space-y-4">
            {entries.map((entry: any, index: number) => (
              <li
                key={`${entry.userId}-${entry.snippetId}-${index}`}
                className="bg-[#0a1b44] p-4 rounded-xl shadow-md flex justify-between items-center hover:scale-[1.01] transition-transform duration-200"
              >
                <div className="flex items-center gap-3">
                  <span className="text-[#A0FF70] font-bold text-xl min-w-[2.5rem] text-center">
                    {medalEmoji(index)}
                  </span>
                  <span className="font-medium text-lg">
                    {entry.userName ?? entry.userId}
                  </span>
                </div>
                <div className="text-[#A0FF70] font-bold text-lg">
                  {entry.score} pts
                </div>
              </li>
            ))}
          </ul>
        )}
      </main>

      <Footer />
    </div>
  );
}
