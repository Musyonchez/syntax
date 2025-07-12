// components/home/LeaderboardCTA.tsx

import Link from "next/link";

const LeaderboardCTA = () => (
  <section className="bg-[#A0FF70] text-black py-20 px-6">
    <div className="max-w-4xl mx-auto text-center">
      <h2 className="text-3xl font-bold mb-4">🏆 Who’s at the Top?</h2>
      <p className="mb-8 text-lg text-gray-800">
        Whether you’re here to sharpen your skills or outpace your friends,
        SyntaxMem’s Leaderboard lets you track your progress, earn ranks, and
        see how you stack up globally.
      </p>
      <Link
        href="/leaderboard"
        className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
      >
        View Leaderboard
      </Link>
    </div>
  </section>
);

export default LeaderboardCTA;
