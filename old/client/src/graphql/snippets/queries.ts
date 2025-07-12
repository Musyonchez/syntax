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
  query GetSnippet($id: String!, $ifmask: Boolean = false, $difficulty: Int) {
    getSnippet(id: $id, ifmask: $ifmask, difficulty: $difficulty) {
      id
      title
      content
      language
      userId
      createdAt
      favorite
      solveCount
      maskedContent
      answer
    }
  }
`;

