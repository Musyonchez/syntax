"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { Play, CheckCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const demoSnippet = {
  language: "Python",
  difficulty: 3,
  title: "List Comprehension",
  originalCode: `# Create a list of squares for even numbers from 0 to 10
numbers = [x**2 for x in range(11) if x % 2 == 0]
print(numbers)`,
  maskedCode: `# Create a list of squares for even numbers from 0 to 10
numbers = [x**2 for x in _____(11) if x __ 2 == 0]
print(_______)`,
  blanks: ["range", "%", "numbers"],
  currentBlanks: ["", "", ""],
};

export function DemoSection() {
  const [currentBlankIndex, setCurrentBlankIndex] = useState(0);
  const [userInputs, setUserInputs] = useState(["", "", ""]);
  const [showResult, setShowResult] = useState(false);
  const [isDemo, setIsDemo] = useState(false);

  const startDemo = () => {
    setIsDemo(true);
    setCurrentBlankIndex(0);
    setUserInputs(["", "", ""]);
    setShowResult(false);

    // Auto-fill demonstration
    const fillBlanks = async () => {
      for (let i = 0; i < demoSnippet.blanks.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 1500));
        setCurrentBlankIndex(i);
        setUserInputs((prev) => {
          const newInputs = [...prev];
          newInputs[i] = demoSnippet.blanks[i];
          return newInputs;
        });
      }
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setShowResult(true);
    };

    fillBlanks();
  };

  const resetDemo = () => {
    setIsDemo(false);
    setCurrentBlankIndex(0);
    setUserInputs(["", "", ""]);
    setShowResult(false);
  };

  const renderCodeWithBlanks = () => {
    const code = demoSnippet.maskedCode;
    let blankIndex = 0;

    return code.split("_____").map((part, index) => {
      if (index === 0) return part;

      const currentInput = userInputs[blankIndex] || "";
      const isCorrect = currentInput === demoSnippet.blanks[blankIndex];
      const isCurrent = currentBlankIndex === blankIndex && isDemo;

      blankIndex++;

      return (
        <span key={index}>
          <span
            className={`inline-block min-w-[80px] rounded px-2 py-1 border-2 transition-all ${
              isCurrent
                ? "border-primary bg-primary/10 animate-pulse"
                : showResult
                  ? isCorrect
                    ? "border-green-500 bg-green-500/10"
                    : "border-red-500 bg-red-500/10"
                  : "border-muted bg-muted/50"
            }`}
          >
            {currentInput || (isCurrent ? "..." : "___")}
          </span>
          {part}
        </span>
      );
    });
  };

  return (
    <section className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              See It In Action
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Experience how SyntaxMem helps you learn through interactive code
              completion
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            viewport={{ once: true }}
            className="mt-12"
          >
            <Card className="mx-auto max-w-3xl">
              <CardHeader className="flex flex-col-reverse gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-center max-sm:justify-center max-sm:w-full sm:gap-3">
                  <CardTitle className="text-xl text-center sm:text-left">
                    {demoSnippet.title}
                  </CardTitle>
                  <div className="flex items-center gap-2 max-sm:justify-center max-sm:w-full">
                    <Badge variant="secondary">{demoSnippet.language}</Badge>
                    <Badge variant="outline">
                      Difficulty: {demoSnippet.difficulty}/10
                    </Badge>
                  </div>
                </div>
                {!isDemo ? (
                  <Button
                    onClick={startDemo}
                    className="gap-2 w-full sm:w-auto"
                  >
                    <Play className="h-4 w-4" />
                    Try Demo
                  </Button>
                ) : (
                  <Button
                    variant="outline"
                    onClick={resetDemo}
                    className="w-full sm:w-auto"
                  >
                    Reset
                  </Button>
                )}
              </CardHeader>
              <CardContent>
                <div className="rounded-lg border bg-background p-6 overflow-x-auto">
                  <pre className="text-sm font-mono leading-relaxed whitespace-pre-wrap break-words min-w-0">
                    <code className="block">{renderCodeWithBlanks()}</code>
                  </pre>
                </div>

                {showResult && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="mt-6 rounded-lg border-2 border-green-500/20 bg-green-500/5 p-4"
                  >
                    <div className="flex items-center gap-2 text-green-600 mb-3">
                      <CheckCircle className="h-5 w-5" />
                      <span className="font-semibold">
                        Perfect! Challenge Complete
                      </span>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      <div className="mb-2">
                        <strong>Output:</strong> [0, 4, 16, 36, 64, 100]
                      </div>
                      <div>
                        <strong>Score:</strong> 100/100 • <strong>Time:</strong>{" "}
                        2.3s • <strong>Accuracy:</strong> 100%
                      </div>
                    </div>
                  </motion.div>
                )}

                {!showResult && (
                  <div className="mt-6 text-center text-sm text-muted-foreground">
                    {isDemo
                      ? "Watching the demo... blanks are being filled automatically"
                      : "Click 'Try Demo' to see how code completion works"}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            viewport={{ once: true }}
            className="mt-12 grid gap-6 md:grid-cols-3"
          >
            <div className="text-center">
              <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-500/10">
                <span className="text-2xl">1️⃣</span>
              </div>
              <h3 className="font-semibold">Choose Challenge</h3>
              <p className="text-sm text-muted-foreground">
                Select from 1000+ code snippets across multiple languages
              </p>
            </div>
            <div className="text-center">
              <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-500/10">
                <span className="text-2xl">2️⃣</span>
              </div>
              <h3 className="font-semibold">Fill the Blanks</h3>
              <p className="text-sm text-muted-foreground">
                Complete the missing code with instant syntax validation
              </p>
            </div>
            <div className="text-center">
              <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-lg bg-green-500/10">
                <span className="text-2xl">3️⃣</span>
              </div>
              <h3 className="font-semibold">Get Feedback</h3>
              <p className="text-sm text-muted-foreground">
                Receive detailed scoring and improve your ranking
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

