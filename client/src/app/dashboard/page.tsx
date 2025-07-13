import { Metadata } from "next"
import { ComingSoon } from "@/components/common/coming-soon"

export const metadata: Metadata = {
  title: "Dashboard",
  description: "View your coding progress, statistics, and achievements on your personal SyntaxMem dashboard.",
}

export default function DashboardPage() {
  return (
    <ComingSoon
      title="Personal Dashboard"
      description="Track your coding journey with detailed statistics, progress charts, and personalized insights to help you improve."
      features={[
        "Practice session statistics",
        "Language proficiency tracking",
        "Achievement gallery",
        "Learning streaks and goals",
        "Performance analytics",
        "Personalized recommendations"
      ]}
      estimatedDate="Phase 2 - Core Practice Features"
    />
  )
}