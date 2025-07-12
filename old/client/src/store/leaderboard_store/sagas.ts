import { call, put, takeEvery } from "redux-saga/effects";
import {
  FETCH_LEADERBOARD,
  SET_LEADERBOARD,
  SET_FETCH_LEADERBOARD_STATUS,
  SET_ADD_LEADERBOARD_STATUS,
  ADD_LEADERBOARD,
} from "./actions"; // Adjust path if needed

import { GET_LEADERBOARD } from "../../graphql/leaderboard/queries";
import { ADD_LEADERBOARD as ADD_LEADERBOARD_MUT } from "../../graphql/leaderboard/mutation";
import apolloClient from "../../apollo/client";

function* fetchLeaderboardSaga(action: any) {
  try {
    yield put({ type: SET_FETCH_LEADERBOARD_STATUS, payload: "loading" });

    const category = action.payload;

    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_LEADERBOARD,
      variables: { category },
    });

    if (data.getLeaderboard && data.getLeaderboard.category) {
      console.log(data.getLeaderboard);
      yield put({ type: SET_LEADERBOARD, payload: data.getLeaderboard });
      yield put({ type: SET_FETCH_LEADERBOARD_STATUS, payload: "success" });
    } else {
      yield put({ type: SET_FETCH_LEADERBOARD_STATUS, payload: "not_found" });
    }
  } catch (error) {
    console.error("Fetch leaderboard failed:", error);
    yield put({ type: SET_FETCH_LEADERBOARD_STATUS, payload: "error" });
  }
}

function* addLeaderboardSaga(action: any) {
  try {
    yield put({ type: SET_ADD_LEADERBOARD_STATUS, payload: "loading" });
    console.log(action.payload)
    yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_LEADERBOARD_MUT,
      variables: action.payload,
    });

    yield put({ type: SET_ADD_LEADERBOARD_STATUS, payload: "success" });
  } catch (error) {
    console.error("Add leaderboard failed:", error);
    yield put({ type: SET_ADD_LEADERBOARD_STATUS, payload: "error" });
  }
}

export default function* rootSaga() {
  yield takeEvery(FETCH_LEADERBOARD, fetchLeaderboardSaga);
  yield takeEvery(ADD_LEADERBOARD, addLeaderboardSaga);
}
