// action types for users
export const FETCH_USERS = "FETCH_USERS";
export const SET_USERS = "SET_USERS";
export const FETCH_USER = "FETCH_USER";
export const SET_USER = "SET_USER";
export const ADD_USER = "ADD_USER";
export const SET_ADD_USER_STATUS = "SET_ADD_USER_STATUS";


// User payload interface
export interface UserPayload {
  username: string;
  email: string;
  image: string;
  createdAt: string;
}


// User action creators
export const fetchUsers = () => ({ type: FETCH_USERS });

export const setUsers = (users: any[]) => ({
  type: SET_USERS,
  payload: users,
});

export const fetchUser = (email: string) => ({
  type: FETCH_USER,
  payload: { email },
});

export const setUser = (user: any) => ({
  type: SET_USER,
  payload: user,
});

export const addUser = (payload: UserPayload) => ({
  type: ADD_USER,
  payload,
});

export const setAddUserStatus = (status: "idle" | "loading" | "success" | "error" ) => ({
  type: SET_ADD_USER_STATUS,
  payload: status,
});
