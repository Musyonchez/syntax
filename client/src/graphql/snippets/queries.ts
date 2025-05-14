import { gql } from "@apollo/client";

export const GET_SNIPPETS = gql`
  query GetSnippets {
    getSnippets {
      id
      title
      content
      language
      userId
      createdAt
      favorite
      solveCount
    }
  }
`;
