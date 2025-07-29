export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-8rem)] p-8">
      {/* Hero Section */}
      <div className="text-center space-y-8 max-w-2xl">
        <h1 className="text-4xl sm:text-6xl font-bold text-foreground">
          SyntaxMem
        </h1>
        
        <p className="text-xl text-muted-foreground">
          Master coding through interactive masked code completion.
          Fill in the blanks, improve your skills.
        </p>
        
        <div className="space-y-4">
          <p className="text-muted-foreground">
            Choose elegant solutions over complex ones.
          </p>
          <p className="text-sm text-muted-foreground/80">
            Practice with real code snippets where keywords and functions are masked based on difficulty.
            Build muscle memory through repetition and pattern recognition.
          </p>
        </div>
      </div>
    </div>
  )
}