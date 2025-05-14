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

export const GET_SNIPPET = gql`
  query GetSnippet($id: String!) {
    getSnippet(id: $id) {
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
