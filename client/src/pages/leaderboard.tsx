import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/store";
import {
  fetchLeaderboard,
  setFetchLeaderboardStatus,
} from "@/store/leaderboard_store/actions";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import LeaderboardFilters from "@/components/leaderboard/Filters";
import LeaderboardStatus from "@/components/leaderboard/Status";
import LeaderboardEntries from "@/components/leaderboard/Entries";

const VALID_LANGUAGES = ["Python", "Javascript"];
const VALID_TIME_CATEGORIES = ["daily", "weekly", "monthly", "half-yearly", "yearly", "all-time"];

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

        <LeaderboardFilters
          selectedTime={selectedTime}
          selectedLanguage={selectedLanguage}
          setSelectedTime={setSelectedTime}
          setSelectedLanguage={setSelectedLanguage}
          validTimes={VALID_TIME_CATEGORIES}
          validLanguages={VALID_LANGUAGES}
        />

        <p className="mb-6 text-gray-300 text-center text-lg">
          Current Category:{" "}
          <span className="text-white font-semibold">
            🏆 {selectedTime.charAt(0).toUpperCase() + selectedTime.slice(1)}{" "}
            {selectedLanguage.charAt(0).toUpperCase() + selectedLanguage.slice(1)}
          </span>
        </p>

        <LeaderboardStatus status={fetchLeaderboardStatus} />
        {entries.length > 0 && <LeaderboardEntries entries={entries} />}
      </main>
      <Footer />
    </div>
  );
}
