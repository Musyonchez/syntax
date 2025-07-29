import { Metadata } from "next"
import { ComingSoon } from "@/components/common/coming-soon"

export const metadata: Metadata = {
  title: "Code Snippets",
  description: "Browse, create, and manage code snippets for practice challenges in multiple programming languages.",
}

export default function SnippetsPage() {
  return (
    <ComingSoon
      title="Code Snippets Library"
      description="Browse thousands of code snippets, create your own challenges, and contribute to the SyntaxMem learning community."
      features={[
        "Browse official code snippets",
        "Create personal practice challenges",
        "Submit snippets for review",
        "Filter by language and difficulty",
        "Community ratings and feedback",
        "Advanced search and tagging"
      ]}
      estimatedDate="Phase 2 - Core Practice Features"
    />
  )
}