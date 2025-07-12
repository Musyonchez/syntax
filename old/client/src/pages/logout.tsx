import React from "react";
import { useRouter } from "next/router";
import { useSession, signOut } from "next-auth/react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const Logout = () => {
  const router = useRouter();
  const { data: session } = useSession();

  return (
    <div className="min-h-screen flex flex-col justify-between h-full">
      <Navbar />
      <div className="flex flex-col flex-grow items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          😢 Sad to see you go, {session?.user?.name || "friend"}...
        </h1>
        <p className="text-lg md:text-xl mb-8 max-w-xl">
          We hope you had a good time while you were logged in. Come back soon —
          the code misses you already! 💻❤️
        </p>
        <button
          onClick={() => signOut({ callbackUrl: "/" })}
          className="bg-red-500 hover:bg-red-600 text-white font-semibold px-6 py-3 rounded-xl shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
        >
          Confirm Logout
        </button>
        <p className="mt-6 text-sm text-gray-400 italic">
          “Every logout is just a pause until we meet again.” — The Server 🖥️
        </p>
      </div>
      <Footer />
    </div>
  );
};

export default Logout;
