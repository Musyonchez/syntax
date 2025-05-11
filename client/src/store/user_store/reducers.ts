import { SET_USERS, SET_USER, SET_ADD_USER_STATUS } from "./actions";

// Initial state for users
const initialState = {
  users: [],
  user: null, // user state for single user
  addUserStatus: "idle", // added
};

// User reducer
export default function reducer(state = initialState, action: any) {
  switch (action.type) {
    case SET_USERS:
      return { ...state, users: action.payload };
    case SET_USER:
      return { ...state, user: action.payload }; // Update single user state
    case SET_ADD_USER_STATUS:
      return { ...state, addUserStatus: action.payload };
    default:
      return state;
  }
}
