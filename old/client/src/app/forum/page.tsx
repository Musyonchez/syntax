import { Metadata } from "next"
import { ComingSoon } from "@/components/common/coming-soon"

export const metadata: Metadata = {
  title: "Forum",
  description: "Connect with the SyntaxMem community, discuss coding challenges, and get help from other developers.",
}

export default function ForumPage() {
  return (
    <ComingSoon
      title="Developer Forum"
      description="Connect with fellow developers, discuss coding challenges, share solutions, and get help from the SyntaxMem community."
      features={[
        "Discussion threads by topic",
        "Code sharing and reviews",
        "Q&A with the community",
        "Voting on posts and answers",
        "Expert developer responses",
        "Learning resources sharing"
      ]}
      estimatedDate="Phase 3 - Community Features"
    />
  )
}