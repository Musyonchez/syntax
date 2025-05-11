// src/pages/_app.tsx

import { SessionProvider } from "next-auth/react";
import "@/styles/globals.css";
import { AppProps } from "next/app";
import { ApolloProvider } from "@apollo/client";
import apolloClient from "../apollo/client";
import store from "../store";
import { Provider } from "react-redux";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SessionProvider session={pageProps.session}>
      <ApolloProvider client={apolloClient}>
        <Provider store={store}>
          <Component {...pageProps} />
        </Provider>
      </ApolloProvider>
    </SessionProvider>
  );
}

export default MyApp;
