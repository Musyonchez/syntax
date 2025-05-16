// actions.ts
export const FETCH_SNIPPETS = "FETCH_SNIPPETS";
export const SET_SNIPPETS = "SET_SNIPPETS";
export const FETCH_SNIPPET = "FETCH_SNIPPET";
export const SET_SNIPPET = "SET_SNIPPET";
export const SET_FETCH_SNIPPET_STATUS = "SET_FETCH_SNIPPET_STATUS";
export const ADD_SNIPPET = "ADD_SNIPPET";
export const SET_ADD_SNIPPET_STATUS = "SET_ADD_SNIPPET_STATUS";
export const ADD_FAVORITE = "ADD_FAVORITE";
export const SET_ADD_FAVORITE_STATUS = "SET_ADD_FAVORITE_STATUS";

export interface SnippetPayload {
  title: string;
  content: string;
  language: string;
  createdAt: string;
  userId: string;
}
export const fetchSnippets = () => ({ type: FETCH_SNIPPETS });

export const setSnippets = (snippets: any[]) => ({
  type: SET_SNIPPETS,
  payload: snippets,
});

export const fetchSnippet = (
  id: string,
  ifmask: boolean = false,
  difficulty?: number
) => ({
  type: FETCH_SNIPPET,
  payload: { id, ifmask, difficulty },
});

export const setSnippet = (snippet: any[]) => ({
  type: SET_SNIPPET,
  payload: snippet,
});

export const setFetchSnippetStatus = (
  status: "idle" | "loading" | "success" | "error" | "not_found"
) => ({
  type: SET_FETCH_SNIPPET_STATUS,
  payload: status,
});

export const addSnippet = (payload: SnippetPayload) => ({
  type: ADD_SNIPPET,
  payload,
});

export const setAddSnippetStatus = (
  status: "idle" | "loading" | "success" | "error"
) => ({
  type: SET_ADD_SNIPPET_STATUS,
  payload: status,
});

export const addFavorite = (
  id: number,
  type: "single" | "group" = "single"
) => ({
  type: ADD_FAVORITE,
  payload: { id, type },
});

export const setAddFavoriteStatus = (
  status: "idle" | "loading" | "success" | "error"
) => ({
  type: SET_ADD_FAVORITE_STATUS,
  payload: status,
});
