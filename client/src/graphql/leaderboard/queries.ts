import { gql } from "@apollo/client";

// Existing user queries...

export const GET_LEADERBOARD = gql`
  query GetLeaderboard($category: String!) {
    getLeaderboard(category: $category) {
      category
      entries {
        userId
        userName
        snippetId
        score
        similarity
        difficulty
        dateOfSubmission
      }
    }
  }
`;

