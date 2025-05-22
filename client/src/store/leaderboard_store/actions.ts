// actions/leaderboardActions.ts
export const FETCH_LEADERBOARD = "FETCH_LEADERBOARD";
export const SET_LEADERBOARD = "SET_LEADERBOARD";
export const SET_FETCH_LEADERBOARD_STATUS = "SET_FETCH_LEADERBOARD_STATUS";
export const ADD_LEADERBOARD = "ADD_LEADERBOARD_ENTRY";
export const SET_ADD_LEADERBOARD_STATUS = "SET_ADD_LEADERBOARD_STATUS";

export interface LeaderboardEntryPayload {
  language: string;
  userId: string;
  userName: string;
  snippetId: string;
  score: number;
  similarity: number;
  difficulty: number;
  dateOfSubmission: string;
}

export const fetchLeaderboard = (category: string) => ({
  type: FETCH_LEADERBOARD,
  payload: category,
});

export const setLeaderboard = (leaderboard: any) => ({
  type: SET_LEADERBOARD,
  payload: leaderboard,
});

export const setFetchLeaderboardStatus = (
  status: "idle" | "loading" | "success" | "error" | "not_found"
) => ({
  type: SET_FETCH_LEADERBOARD_STATUS,
  payload: status,
});

export const addLeaderboardEntry = (payload: LeaderboardEntryPayload) => ({
  type: ADD_LEADERBOARD,
  payload,
});

export const setAddLeaderboardStatus = (
  status: "idle" | "loading" | "success" | "error"
) => ({
  type: SET_ADD_LEADERBOARD_STATUS,
  payload: status,
});
