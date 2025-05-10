import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import Image from "next/image";

const Home = () => {
  return (
    <div className="bg-[#000d2a] text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="bg-[#A0FF70] text-black py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6">
            Master Syntax, One Snippet at a Time
          </h1>
          <p className="text-lg mb-8">
            Struggling to remember code syntax? <strong>SyntaxMem</strong> turns
            your code into interactive fill-in-the-blank quizzes—making recall
            fast, fun, and frustration-free.
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

      {/* How It Works */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-semibold mb-10">How SyntaxMem Works</h2>
          <ol className="space-y-6 text-left">
            <li>
              <strong>1. Add Code</strong> – Go to{" "}
              <code className="text-yellow-400 underline font-extrabold italic">
                quiz
              </code>
              and paste a code snippet you'd like to memorize.
            </li>
            <li>
              <strong>2. Smart Masking</strong> – We hide key syntax elements
              like keywords and operators automatically.
            </li>
            <li>
              <strong>3. Practice & Progress</strong> – Visit{" "}
              <code className="text-yellow-400 underline font-extrabold italic">
                practice
              </code>{" "}
              and fill in the blanks to strengthen memory through repetition.
            </li>
            <li>
              <strong>4. Track Your Rank</strong> – Compete with others on the{" "}
              <code className="text-yellow-400 underline font-extrabold italic">
                leaderboard
              </code>{" "}
              and climb the ranks!
            </li>
          </ol>
        </div>
      </section>

      {/* Demo Snippet Section */}
      <section className="bg-[#A0FF70] text-black py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-2xl font-bold mb-6">
            Try It Out – No Sign Up Needed
          </h3>

          <div className=" flex justify-around items-center">
            <div className="text-left bg-white p-6 rounded-lg shadow-md w-[300px]">
              <h4 className="text-lg font-semibold mb-2">Sample Code:</h4>
              <pre className="bg-gray-100 text-black p-4 rounded-md overflow-auto">
                {`for i in range(5):
    print(i)`}
              </pre>
            </div>

            <div className="text-left bg-white p-6 rounded-lg shadow-md">
              <h4 className="text-lg font-semibold mb-2">
                Masked Quiz Version:
              </h4>
              <pre className="bg-gray-100 text-black p-4 rounded-md overflow-auto">
                {`for i (____) (____)(5):
    print(____)`}
              </pre>
            </div>
          </div>

          <p className="mt-4 text-sm text-gray-700">
            Just a taste! This is how your custom snippets will look when turned
            into a quiz.
          </p>
        </div>
      </section>

      {/* Screenshot Section */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">See It in Action</h2>
          <p className="mb-8 max-w-2xl mx-auto text-gray-300">
            Here's what the Practice page looks like once your snippet is
            converted. It's clean, focused, and ready to test your recall.
          </p>
          <div className="shadow-lg rounded-lg overflow-hidden border border-[#A0FF70]">
            <Image
              src="/images/practice-screenshot.png"
              alt="Practice Quiz Screenshot"
              width={1000}
              height={600}
              className="w-full h-auto"
            />
          </div>
        </div>
      </section>

      {/* Leaderboard Section */}
      <section className="bg-[#A0FF70] text-black py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">🏆 Who’s at the Top?</h2>
          <p className="mb-8 text-lg text-gray-800">
            Whether you’re here to sharpen your skills or outpace your friends,
            SyntaxMem’s Leaderboard lets you track your progress, earn ranks,
            and see how you stack up globally.
          </p>
          <Link
            href="/leaderboard"
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
          >
            View Leaderboard
          </Link>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-6">Ready to Code Smarter?</h2>
          <p className="text-lg mb-8">
            Add your first snippet and start turning repetition into intuition.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/add_snippet"
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
            >
              Add a Snippet
            </Link>
            <Link
              href="/login"
              className="border border-blue-600 text-blue-600 px-6 py-3 rounded-md hover:bg-blue-700 hover:text-white"
            >
              Log In
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Home;
