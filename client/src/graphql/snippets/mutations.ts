import { gql } from "@apollo/client";

export const ADD_SNIPPET = gql`
  mutation AddSnippet(
    $title: String!
    $content: String!
    $language: String!
    $createdAt: String!
    $userId: String!
  ) {
    addSnippet(
      title: $title
      content: $content
      language: $language
      createdAt: $createdAt
      userId: $userId
    ) {
      id
      title
      content
      language
    }
  }
`;