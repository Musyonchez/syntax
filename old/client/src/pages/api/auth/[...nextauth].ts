// import NextAuth from "next-auth";
// import GoogleProvider from "next-auth/providers/google";

// export default NextAuth({
//   providers: [
//     GoogleProvider({
//       clientId: process.env.GOOGLE_CLIENT_ID!,
//       clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
//     }),
//   ],
//   secret: process.env.NEXTAUTH_SECRET,
//   pages: {
//     signIn: "/login",
//   },
//   session: {
//     strategy: "jwt", // or "database" if you're storing sessions
//     maxAge: 30 * 24 * 60 * 60, // 💡 30 days in seconds
//     updateAge: 24 * 60 * 60,   // 🕒 Update session token every 24h
//   },
//   jwt: {
//     maxAge: 30 * 24 * 60 * 60, // Optional but recommended for jwt strategy
//   },
// });


import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt", // or "database" if you're storing sessions
    maxAge: 30 * 24 * 60 * 60, // 💡 30 days in seconds
    updateAge: 24 * 60 * 60,   // 🕒 Update session token every 24h
  },
  jwt: {
    maxAge: 30 * 24 * 60 * 60, // Optional but recommended for jwt strategy
  },
  logger: {
    error(code, ...message) {
      console.error(code, ...message);
    },
    warn(code, ...message) {
      console.warn(code, ...message);
    },
    debug(code, ...message) {
      console.debug(code, ...message);
    }
  }
});
