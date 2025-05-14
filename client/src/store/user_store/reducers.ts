import { SET_USERS, SET_USER, SET_ADD_USER_STATUS } from "./actions";


const initialState = {
  users: [],
  user: null, 
  addUserStatus: "idle",
};

// User reducer
export default function reducer(state = initialState, action: any) {
  switch (action.type) {
    case SET_USERS:
      return { ...state, users: action.payload };
    case SET_USER:
      if (JSON.stringify(state.user) === JSON.stringify(action.payload)) {
        return state;
      }
      return { ...state, user: action.payload };
    case SET_ADD_USER_STATUS:
      return { ...state, addUserStatus: action.payload };
    default:
      return state;
  }
}
