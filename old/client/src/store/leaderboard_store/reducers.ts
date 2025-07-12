// Import leaderboard action types at the top with others
import {
  SET_LEADERBOARD,
  SET_FETCH_LEADERBOARD_STATUS,
  SET_ADD_LEADERBOARD_STATUS,
} from "./actions";

const initialState = {
  leaderboard: {} as Record<string, { category: string; entries: any[] }>,
  fetchLeaderboardStatus: "idle",
  addLeaderboardStatus: "idle",
};

export default function reducer(state = initialState, action: any) {
  switch (action.type) {
    // Leaderboard cases
    case SET_LEADERBOARD:
      return {
        ...state,
        leaderboard: {
          ...state.leaderboard,
          [action.payload.category]: action.payload,
        },
      };
    case SET_FETCH_LEADERBOARD_STATUS:
      return { ...state, fetchLeaderboardStatus: action.payload };
    case SET_ADD_LEADERBOARD_STATUS:
      return { ...state, addLeaderboardStatus: action.payload };

    default:
      return state;
  }
}
