import { ApolloClient, InMemoryCache } from "@apollo/client";

const client = new ApolloClient({
  uri: "http://localhost:8000/graphql", // Adjust this URL as needed
  cache: new InMemoryCache(),
});

export default client;
