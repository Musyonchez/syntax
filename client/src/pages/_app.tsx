import "@/styles/globals.css";
import { AppProps } from "next/app";
import { ApolloProvider } from "@apollo/client";
import apolloClient from "../apollo/client";
import { Provider } from "../store";
import store from "../store";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ApolloProvider client={apolloClient}>
      <Provider store={store}>
        <Component {...pageProps} />
      </Provider>
    </ApolloProvider>
  );
}

export default MyApp;
