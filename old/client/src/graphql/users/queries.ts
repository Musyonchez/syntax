import { gql } from "@apollo/client";

export const GET_USERS = gql`
  query GetUsers {
    getUsers {
      id
      username
      email
      createdAt
    }
  }
`;



export const GET_USER = gql`
  query GetUser($email: String!) {
    getUser(email: $email) {
      id
      username
      email
      image
      createdAt
    }
  }
`;
