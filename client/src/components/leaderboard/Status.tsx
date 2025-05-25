// components/leaderboard/Status.tsx
interface StatusProps {
    status: string;
  }
  
  export default function LeaderboardStatus({ status }: StatusProps) {
    if (status === "loading") return <p className="text-gray-400 text-center">⏳ Loading leaderboard...</p>;
    if (status === "error") return <p className="text-red-400 text-center">❌ Failed to fetch leaderboard.</p>;
    if (status === "not_found") return <p className="text-yellow-400 text-center">⚠️ No data found.</p>;
    return null;
  }
  