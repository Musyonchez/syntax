"use client"

import { motion } from "framer-motion"
import { CheckCircle, Clock, Code } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ComingSoonProps {
  title: string
  description: string
  features?: string[]
  estimatedDate?: string
}

export function ComingSoon({ 
  title, 
  description, 
  features = [], 
  estimatedDate = "Coming Soon" 
}: ComingSoonProps) {
  return (
    <div className="container mx-auto px-4 py-20">
      <div className="mx-auto max-w-4xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-full bg-primary/10">
            <Code className="h-10 w-10 text-primary" />
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl mb-6">
            {title}
          </h1>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            {description}
          </p>

          <div className="flex items-center justify-center gap-2 mb-12">
            <Clock className="h-5 w-5 text-primary" />
            <span className="text-lg font-semibold text-primary">{estimatedDate}</span>
          </div>
        </motion.div>

        {features.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="mx-auto max-w-2xl">
              <CardHeader>
                <CardTitle>What&apos;s Coming</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {features.map((feature, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: 0.3 + index * 0.1 }}
                      className="flex items-center gap-3 text-left"
                    >
                      <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                      <span>{feature}</span>
                    </motion.li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        )}

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-12 flex flex-col gap-4 sm:flex-row sm:justify-center"
        >
          <Link href="/">
            <Button size="lg">
              Back to Home
            </Button>
          </Link>
          <Link href="/auth/signin">
            <Button variant="outline" size="lg">
              Sign Up for Updates
            </Button>
          </Link>
        </motion.div>
      </div>
    </div>
  )
}