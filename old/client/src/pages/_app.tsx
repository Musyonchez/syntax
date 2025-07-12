// src/pages/_app.tsx

import { SessionProvider } from "next-auth/react";
import "@/styles/globals.css";
import { AppProps } from "next/app";
import { ApolloProvider } from "@apollo/client";
import apolloClient from "../apollo/client";
import store from "../store";
import { Provider } from "react-redux";

import { Toaster } from "react-hot-toast"; // <-- import toaster

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SessionProvider session={pageProps.session}>
      <ApolloProvider client={apolloClient}>
        <Provider store={store}>
          <>
            <Component {...pageProps} />
            <Toaster 
              position="top-right" 
              toastOptions={{
                style: {
                  background: "#333",
                  color: "#fff",
                },
                success: {
                  duration: 3000,
                  iconTheme: {
                    primary: "green",
                    secondary: "black",
                  },
                },
                error: {
                  duration: 4000,
                  iconTheme: {
                    primary: "red",
                    secondary: "black",
                  },
                },
              }}
            />
          </>
        </Provider>
      </ApolloProvider>
    </SessionProvider>
  );
}

export default MyApp;
