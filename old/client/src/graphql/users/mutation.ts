import { gql } from "@apollo/client";

export const ADD_USER = gql`
  mutation AddUser(
    $username: String!
    $email: String!
    $image: String!
    $createdAt: String!
  ) {
    addUser(
      username: $username
      email: $email
      image: $image
      createdAt: $createdAt
    ) {
      id
      username
      email
      image
      createdAt
    }
  }
`;
