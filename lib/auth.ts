import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import { SupabaseAdapter } from '@auth/supabase-adapter';

const { auth, signIn, signOut } = NextAuth({
  adapter: SupabaseAdapter({
    url: process.env.SUPABASE_URL!,
    secret: process.env.SUPABASE_SERVICE_ROLE_KEY!,
  }),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  pages: {
    signIn: '/login',
    error: '/error',
  },
  session: {
    strategy: 'database',
  },
  debug: process.env.NODE_ENV === 'development',
});

export { auth, signIn, signOut };