// action types for snippets
export const FETCH_SNIPPETS = "FETCH_SNIPPETS";
export const SET_ADD_SNIPPET_STATUS = "SET_ADD_SNIPPET_STATUS";
export const SET_SNIPPETS = "SET_SNIPPETS";
export const ADD_SNIPPET = "ADD_SNIPPET";

// action types for users
export const FETCH_USERS = "FETCH_USERS";
export const SET_USERS = "SET_USERS";
export const FETCH_USER = "FETCH_USER";
export const SET_USER = "SET_USER";
export const ADD_USER = "ADD_USER";
export const SET_ADD_USER_STATUS = "SET_ADD_USER_STATUS";

// Snippet payload interface
export interface SnippetPayload {
  title: string;
  content: string;
  language: string;
  createdAt: string;
  userId: number;
}

// User payload interface
export interface UserPayload {
  username: string;
  email: string;
  password: string;
}

// Snippet action creators
export const fetchSnippets = () => ({ type: FETCH_SNIPPETS });

export const setSnippets = (snippets: any[]) => ({
  type: SET_SNIPPETS,
  payload: snippets,
});

export const addSnippet = (payload: SnippetPayload) => ({
  type: ADD_SNIPPET,
  payload,
});

export const setAddSnippetStatus = (status: "idle" | "loading" | "success" | "error") => ({
  type: SET_ADD_SNIPPET_STATUS,
  payload: status,
});

// User action creators
export const fetchUsers = () => ({ type: FETCH_USERS });

export const setUsers = (users: any[]) => ({
  type: SET_USERS,
  payload: users,
});

export const fetchUser = (id: number) => ({
  type: FETCH_USER,
  payload: { id },
});

export const setUser = (user: any) => ({
  type: SET_USER,
  payload: user,
});

export const addUser = (payload: UserPayload) => ({
  type: ADD_USER,
  payload,
});

export const setAddUserStatus = (status: "idle" | "loading" | "success" | "error") => ({
  type: SET_ADD_USER_STATUS,
  payload: status,
});
