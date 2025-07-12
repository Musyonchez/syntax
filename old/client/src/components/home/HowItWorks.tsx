// components/home/HowItWorks.tsx
const HowItWorks = () => (
  <section className="py-20 px-6">
    <div className="max-w-4xl mx-auto text-center">
      <h2 className="text-3xl font-semibold mb-10 max-sm:text-left">
        How SyntaxMem Works
      </h2>
      <ol className="space-y-6 text-left">
        <li>
          <strong>1. Add Code</strong> – Go to{" "}
          <code className="text-yellow-400 underline font-extrabold italic">
            quiz
          </code>
          and paste a code snippet you'd like to memorize.
        </li>
        <li>
          <strong>2. Smart Masking</strong> – We hide key syntax elements like
          keywords and operators automatically.
        </li>
        <li>
          <strong>3. Practice & Progress</strong> – Visit{" "}
          <code className="text-yellow-400 underline font-extrabold italic">
            practice
          </code>
          and fill in the blanks to strengthen memory through repetition.
        </li>
        <li>
          <strong>4. Track Your Rank</strong> – Compete with others on the{" "}
          <code className="text-yellow-400 underline font-extrabold italic">
            leaderboard
          </code>
          and climb the ranks!
        </li>
      </ol>
    </div>
  </section>
);

export default HowItWorks;

