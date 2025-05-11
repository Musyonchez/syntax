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
  query GetUser($id: Int!) {
    getUser(id: $id) {
      id
      username
      email
      createdAt
    }
  }
`;
