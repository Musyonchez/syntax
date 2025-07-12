// components/home/FinalCTA.tsx

import Link from "next/link";

const FinalCTA = () => (
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
);

export default FinalCTA;
