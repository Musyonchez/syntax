import { gql } from "@apollo/client";

export const ADD_USER = gql`
  mutation AddUser(
    $username: String!
    $email: String!
    $password: String!
    $createdAt: String!
  ) {
    addUser(
      username: $username
      email: $email
      password: $password
      createdAt: $createdAt
    ) {
      id
      username
      email
      createdAt
    }
  }
`;
