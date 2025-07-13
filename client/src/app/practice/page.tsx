import { Metadata } from "next"
import { ComingSoon } from "@/components/common/coming-soon"

export const metadata: Metadata = {
  title: "Practice",
  description: "Practice coding with interactive challenges and improve your programming skills.",
}

export default function PracticePage() {
  return (
    <ComingSoon
      title="Practice Challenges"
      description="Interactive coding practice is coming soon! Complete masked code snippets, get instant feedback, and improve your programming skills."
      features={[
        "Multiple programming languages",
        "Difficulty levels from beginner to expert", 
        "Real-time syntax validation",
        "Instant feedback and scoring",
        "Progress tracking and statistics"
      ]}
    />
  )
}