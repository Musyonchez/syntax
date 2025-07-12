// src/pages/login.tsx
import { signIn, useSession } from "next-auth/react";
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { addUser } from "../store/user_store/actions";
import { RootState } from "../store/";
import { useRouter } from "next/router";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const LoginPage = () => {
  const { data: session } = useSession();
  const router = useRouter();
  const dispatch = useDispatch();
  const status = useSelector((state: RootState) => state.user.addUserStatus);

  useEffect(() => {
    if (session?.user?.email && status === "idle") {
      const newUser = {
        username: session?.user?.name ?? "",
        email: session?.user?.email ?? "",
        image: session?.user?.image ?? "",
        createdAt: new Date().toISOString(),
      };
      dispatch(addUser(newUser));
    }
  }, [session, dispatch]);

  useEffect(() => {
    if (status === "success") {
      router.push("/");
    }
  }, [status, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#000d2a] via-[#001c44] to-[#000d2a] text-white flex flex-col">
      <Navbar />
      <main className="flex-grow flex items-center justify-center px-6 py-20">
        <div className="bg-white/5 backdrop-blur-md border border-white/10 p-10 rounded-2xl shadow-2xl max-w-md w-full text-center space-y-8">
          <h1 className="text-4xl font-bold text-[#A0FF70]">
            🌟 Welcome back, Coder
          </h1>
          <p className="text-lg text-gray-300">
            The snippets' are lonely without you. Let's reconnect and build something legendary.
          </p>

          <button
            onClick={() => signIn("google")}
            className="w-full bg-[#007bff] text-white py-3 rounded-lg text-lg font-semibold hover:bg-[#0056b3] transition duration-300 shadow-md hover:scale-105"
          >
            Sign in with Google
          </button>

          <div className="text-sm text-gray-400 space-y-1">
            {status === "loading" && <p>🔄 Setting things up for you...</p>}
            {status === "error" && (
              <p className="text-red-400">⚠️ Something went wrong. Try again.</p>
            )}
            {status === "success" && (
              <p className="text-green-400">✅ User added! Redirecting...</p>
            )}
            {!session && <p>🔐 Please sign in to access your dashboard.</p>}
          </div>

          <p className="mt-4 text-xs italic text-gray-500">
            “Every login is a promise to your future self.” — The Compiler ⚙️
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default LoginPage;
