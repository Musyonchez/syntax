import { Metadata } from "next"
import { ComingSoon } from "@/components/common/coming-soon"

export const metadata: Metadata = {
  title: "Leaderboard",
  description: "See how you rank against other developers in coding challenges and practice sessions.",
}

export default function LeaderboardPage() {
  return (
    <ComingSoon
      title="Global Leaderboard"
      description="Compete with developers worldwide and see how you rank in coding challenges across different programming languages."
      features={[
        "Global rankings by language",
        "Monthly and all-time leaderboards",
        "Skill level competitions",
        "Achievement tracking",
        "Regional rankings",
        "Team challenges"
      ]}
      estimatedDate="Phase 3 - Community Features"
    />
  )
}