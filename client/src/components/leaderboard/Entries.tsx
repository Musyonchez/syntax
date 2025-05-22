// components/leaderboard/Entries.tsx
const medalEmoji = (index: number) => {
    return ["🥇", "🥈", "🥉"][index] || `#${index + 1}`;
  };
  
  export default function LeaderboardEntries({ entries }: { entries: any[] }) {
    return (
      <ul className="space-y-4">
        {entries.map((entry, index) => (
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
            <div className="text-[#A0FF70] font-bold text-lg">{entry.score} pts</div>
          </li>
        ))}
      </ul>
    );
  }
  