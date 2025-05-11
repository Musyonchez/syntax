// actions.ts
export const FETCH_SNIPPETS = "FETCH_SNIPPETS";
export const SET_ADD_SNIPPET_STATUS = "SET_ADD_SNIPPET_STATUS";
export const SET_SNIPPETS = "SET_SNIPPETS";
export const ADD_SNIPPET = "ADD_SNIPPET";

export interface SnippetPayload {
  title: string;
  content: string;
  language: string;
  createdAt: string;
  userId: number;
}
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
