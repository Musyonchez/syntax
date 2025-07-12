import { gql } from "@apollo/client";

export const ADD_LEADERBOARD = gql`
  mutation AddLeaderboard(
    $language: String!
    $userId: String!
    $userName: String!
    $snippetId: String!
    $score: Float!
    $similarity: Float!
    $difficulty: Int!
    $dateOfSubmission: String!
  ) {
    addLeaderboard(
      language: $language
      userId: $userId
      userName: $userName
      snippetId: $snippetId
      score: $score
      similarity: $similarity
      difficulty: $difficulty
      dateOfSubmission: $dateOfSubmission
    )
  }
`;
