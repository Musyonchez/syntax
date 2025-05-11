import { SET_SNIPPETS } from "./actions";

const initialState = {
  snippets: [],
};

export default function reducer(state = initialState, action: any) {
  switch (action.type) {
    case SET_SNIPPETS:
      return { ...state, snippets: action.payload };
    default:
      return state;
  }
}
