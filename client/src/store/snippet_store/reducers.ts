// reducers.ts
import { SET_SNIPPETS } from "./actions";
import { SET_SNIPPET } from "./actions";
import { SET_FETCH_SNIPPET_STATUS } from "./actions";
import { SET_ADD_SNIPPET_STATUS } from "./actions";

const initialState = {
  snippets: [],
  snippet: null,
  fetchSnippetStatus: "idle",
  addSnippetStatus: "idle",
};

export default function reducer(state = initialState, action: any) {
  switch (action.type) {
    case SET_SNIPPETS:
      return { ...state, snippets: action.payload };
    case SET_SNIPPET:
      if (JSON.stringify(state.snippet) === JSON.stringify(action.payload)) {
        return state;
      }
      return { ...state, snippet: action.payload };
    case SET_FETCH_SNIPPET_STATUS:
      return { ...state, fetchSnippetStatus: action.payload };
    case SET_ADD_SNIPPET_STATUS:
      return { ...state, addSnippetStatus: action.payload };
    default:
      return state;
  }
}
