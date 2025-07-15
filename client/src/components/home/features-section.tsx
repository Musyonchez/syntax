"use client"

import { motion } from "framer-motion"
import { 
  Code2, 
  Zap, 
  Trophy, 
  Users, 
  BookOpen, 
  Target, 
  BarChart3, 
  MessageCircle 
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const features = [
  {
    icon: Code2,
    title: "Multi-Language Support",
    description: "Practice Python, JavaScript, Java, C++, and more programming languages with syntax-specific challenges.",
    color: "bg-blue-500/10 text-blue-600 dark:text-blue-400",
  },
  {
    icon: Target,
    title: "Difficulty Levels",
    description: "From beginner to expert, choose challenges that match your skill level and progressively advance.",
    color: "bg-green-500/10 text-green-600 dark:text-green-400",
  },
  {
    icon: Zap,
    title: "Instant Feedback",
    description: "Get real-time validation, syntax checking, and detailed explanations for every solution.",
    color: "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400",
  },
  {
    icon: BarChart3,
    title: "Progress Tracking",
    description: "Monitor your improvement with detailed analytics, streaks, and performance metrics.",
    color: "bg-purple-500/10 text-purple-600 dark:text-purple-400",
  },
  {
    icon: Trophy,
    title: "Global Leaderboard",
    description: "Compete with developers worldwide and climb the rankings in your favorite languages.",
    color: "bg-orange-500/10 text-orange-600 dark:text-orange-400",
  },
  {
    icon: Users,
    title: "Community Driven",
    description: "Submit your own code snippets and contribute to the growing library of challenges.",
    color: "bg-pink-500/10 text-pink-600 dark:text-pink-400",
  },
  {
    icon: BookOpen,
    title: "Learning Resources",
    description: "Access curated learning materials and explanations for complex programming concepts.",
    color: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400",
  },
  {
    icon: MessageCircle,
    title: "Developer Forum",
    description: "Connect with other developers, discuss solutions, and get help from the community.",
    color: "bg-cyan-500/10 text-cyan-600 dark:text-cyan-400",
  },
]

export function FeaturesSection() {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Everything You Need to Excel
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              A comprehensive platform designed to accelerate your programming journey
            </p>
          </motion.div>

          <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  whileHover={{ scale: 1.02 }}
                  className="group"
                >
                  <Card className="h-full transition-all duration-300 hover:shadow-lg hover:border-primary/20">
                    <CardHeader className="pb-4">
                      <div className={`mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-lg transition-all duration-300 group-hover:scale-110 ${feature.color}`}>
                        <Icon className="h-6 w-6" />
                      </div>
                      <CardTitle className="text-center text-lg">
                        {feature.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <p className="text-center text-sm text-muted-foreground leading-relaxed">
                        {feature.description}
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}