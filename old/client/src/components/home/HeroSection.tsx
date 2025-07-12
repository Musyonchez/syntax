// components/home/HeroSection.tsx

import Link from "next/link";

const HeroSection = () => (
  <section className="bg-[#A0FF70] text-black py-20 px-4">
    <div className="max-w-4xl mx-auto text-center">
      <h1 className="text-5xl font-bold mb-6">
        Master Syntax, One Snippet at a Time
      </h1>
      <p className="text-lg mb-8">
        Struggling to remember code syntax? <strong>SyntaxMem</strong> turns
        your code into interactive fill-in-the-blank quizzes—making recall fast,
        fun, and frustration-free.
      </p>
      <div className="flex flex-wrap justify-center gap-4">
        <Link
          href="/add_snippet"
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
        >
          Get Started
        </Link>
        <Link
          href="/login"
          className="border border-blue-600 text-blue-600 px-6 py-3 rounded-md hover:bg-blue-700 hover:text-white transition"
        >
          Log In
        </Link>
      </div>
    </div>
  </section>
);

export default HeroSection;
