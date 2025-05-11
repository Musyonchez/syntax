// src/pages/login.tsx

import { signIn, useSession } from "next-auth/react";
import { useRouter } from "next/router";
import { useEffect } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const LoginPage = () => {
  const { data: session } = useSession();
  const router = useRouter();

//   useEffect(() => {
//     if (session) {
//       router.push("/"); // Redirect to homepage or dashboard if already logged in
//     }
//   }, [session, router]);

  return (
    <div className="min-h-screen bg-[#000d2a] text-white flex flex-col">
      <Navbar />
      <main className="flex-grow py-16 px-6 max-w-4xl mx-auto">
        <div className="flex flex-col justify-center items-center space-y-6">
          <h1 className="text-4xl font-bold text-center text-[#A0FF70]">Welcome Back</h1>
          <p className="text-center text-lg text-[#A0FF70]">
            Please sign in to continue to your dashboard.
          </p>

          <button
            onClick={() => signIn("google")}
            className="w-full sm:w-64 bg-[#007bff] text-white p-4 rounded-lg text-xl font-semibold hover:bg-[#0056b3] transition duration-300"
          >
            Sign in with Google
          </button>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default LoginPage;

























// src/pages/login.tsx

// import { signIn, useSession } from "next-auth/react";
// import { useRouter } from "next/router";
// import { useEffect } from "react";

// const LoginPage = () => {
//   const { data: session } = useSession();
//   const router = useRouter();

// //   useEffect(() => {
// //     if (session) {
// //       router.push("/"); // Redirect to homepage or dashboard if already logged in
// //     }
// //   }, [session, router]);

//   return (
//     <div>
//       <h1>Login</h1>
//       <button
//         onClick={() => signIn("google")}
//         className="bg-blue-500 text-white p-2 rounded"
//       >
//         Sign in with Google
//       </button>
//     </div>
//   );
// };

// export default LoginPage;
