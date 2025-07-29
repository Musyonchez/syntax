"use client"

import { motion } from "framer-motion"
import { ArrowRight, Code, Sparkles } from "lucide-react"
import Link from "next/link"
import { useSession } from "next-auth/react"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

export function CTASection() {
  const { data: session } = useSession()

  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="mx-auto max-w-4xl"
        >
          <Card className="relative overflow-hidden border-2">
            {/* Background Pattern */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5" />
            <div className="absolute inset-0 bg-grid-black/[0.02] dark:bg-grid-white/[0.02]" />
            
            {/* Floating Elements */}
            <motion.div
              animate={{ 
                y: [0, -10, 0],
                rotate: [0, 5, 0]
              }}
              transition={{ 
                duration: 6,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="absolute top-6 left-6 opacity-20"
            >
              <Code className="h-8 w-8 text-primary" />
            </motion.div>
            
            <motion.div
              animate={{ 
                y: [0, 10, 0],
                rotate: [0, -5, 0]
              }}
              transition={{ 
                duration: 8,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="absolute top-6 right-6 opacity-20"
            >
              <Sparkles className="h-8 w-8 text-secondary" />
            </motion.div>

            <CardContent className="relative p-12 text-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                viewport={{ once: true }}
              >
                <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
                  Ready to Level Up Your Coding Skills?
                </h2>
                <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground">
                  Join thousands of developers who are already improving their programming 
                  skills through interactive practice. Start your journey today!
                </p>

                <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
                  {session ? (
                    <>
                      <Link href="/practice">
                        <Button size="lg" className="text-lg px-8 py-3 gap-2">
                          Continue Your Journey
                          <ArrowRight className="h-5 w-5" />
                        </Button>
                      </Link>
                      <Link href="/dashboard">
                        <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                          View Dashboard
                        </Button>
                      </Link>
                    </>
                  ) : (
                    <>
                      <Link href="/auth/signin">
                        <Button size="lg" className="text-lg px-8 py-3 gap-2">
                          Start Free Today
                          <ArrowRight className="h-5 w-5" />
                        </Button>
                      </Link>
                      <Link href="/practice">
                        <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                          Try Demo First
                        </Button>
                      </Link>
                    </>
                  )}
                </div>

                <div className="mt-8 text-sm text-muted-foreground">
                  <p>✨ Free forever • No credit card required • Join 10,000+ developers</p>
                </div>
              </motion.div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  )
}