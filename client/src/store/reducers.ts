// reducers.ts
import { SET_SNIPPETS } from "./actions";
import { SET_ADD_SNIPPET_STATUS } from "./actions";

const initialState = {
  snippets: [],
  addSnippetStatus: "idle", // ⬅️ added
};


export default function reducer(state = initialState, action: any) {
  switch (action.type) {
    case SET_SNIPPETS:
      return { ...state, snippets: action.payload };
    case SET_ADD_SNIPPET_STATUS:
      return { ...state, addSnippetStatus: action.payload };
    default:
      return state;
  }
}
