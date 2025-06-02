import { call, put, takeLatest } from "redux-saga/effects";
import {
  FETCH_SNIPPET,
  FETCH_SNIPPETS,
  ADD_SNIPPET,
  ADD_FAVORITE,
  DELETE_SNIPPET,
  setSnippet,
  setSnippets,
  setFetchSnippetStatus,
  setAddSnippetStatus,
  setAddFavoriteStatus,
  setDeleteSnippetStatus,
} from "./actions";
import { GET_SNIPPETS, GET_SNIPPET } from "../../graphql/snippets/queries";
import { ADD_SNIPPET as ADD_SNIPPET_MUT } from "../../graphql/snippets/mutations";
import { ADD_FAVORITE as ADD_FAVORITE_MUT } from "../../graphql/snippets/mutations";
import { DELETE_SNIPPET as DELETE_SNIPPET_MUT } from "../../graphql/snippets/mutations";
import apolloClient from "../../apollo/client";

function* fetchSnippetsSaga() {
  const { data } = yield call([apolloClient, apolloClient.query], {
    query: GET_SNIPPETS,
  });
  yield put(setSnippets(data.getSnippets));
}

function* fetchSnippetSaga(action: any) {
  try {
    yield put(setFetchSnippetStatus("loading"));
    const { id, ifmask = false, difficulty = null } = action.payload;

    const variables: Record<string, any> = { id };

    // Only add difficulty if ifmask is true and difficulty is provided
    if (ifmask) {
      variables.ifmask = true;
      if (difficulty !== null) {
        variables.difficulty = difficulty;
      }
    }

    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_SNIPPET,
      variables,
    });

    if (data.getSnippet) {
      console.log(id, ifmask, difficulty, data.getSnippet);
      yield put(setSnippet(data.getSnippet));
      yield put(setFetchSnippetStatus("success"));
    } else {
      yield put(setFetchSnippetStatus("not_found"));
    }
  } catch (error) {
    console.error("Fetch snippet failed:", error);
    yield put(setFetchSnippetStatus("error"));
  }
}

function* addSnippetSaga(action: any) {
  try {
    yield put(setAddSnippetStatus("loading"));

    yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_SNIPPET_MUT,
      variables: action.payload,
    });

    yield call(fetchSnippetsSaga);
    yield put(setAddSnippetStatus("success"));
  } catch (error) {
    console.error("Add snippet failed:", error);
    yield put(setAddSnippetStatus("error"));
  }
}

// New saga for addFavorite mutation
function* addFavoriteSaga(action: any) {
  try {
    yield put(setAddFavoriteStatus("loading"));

    const { id, type = "single" } = action.payload;

    const { data } = yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_FAVORITE_MUT,
      variables: { id, type },
    });

    // data.addFavorite returns either an array of snippets (group) or single snippet array
    if (type === "group") {
      yield put(setSnippets(data.addFavorite));
    } else {
      yield put(setSnippet(data.addFavorite[0])); // single snippet array
    }

    yield put(setAddFavoriteStatus("success"));
  } catch (error) {
    console.error("Add favorite failed:", error);
    yield put(setAddFavoriteStatus("error"));
  }
}

function* deleteSnippetSaga(action: any) {
  try {
    yield put(setDeleteSnippetStatus("loading"));

    const { id, type = "single" } = action.payload;

    const { data } = yield call([apolloClient, apolloClient.mutate], {
      mutation: DELETE_SNIPPET_MUT,
      variables: { id, type },
    });

    // data.addFavorite returns either an array of snippets (group) or single snippet array
    if (type === "group") {
      yield put(setSnippets(data.deleteSnippet));
    } else {
      yield put(setSnippet(data.deleteSnippet[0])); // single snippet array
    }

    yield put(setDeleteSnippetStatus("success"));
  } catch (error) {
    console.error("Delete Snippet failed:", error);
    yield put(setDeleteSnippetStatus("error"));
  }
}

export default function* rootSaga() {
  yield takeLatest(FETCH_SNIPPETS, fetchSnippetsSaga);
  yield takeLatest(FETCH_SNIPPET, fetchSnippetSaga);
  yield takeLatest(ADD_SNIPPET, addSnippetSaga);
  yield takeLatest(ADD_FAVORITE, addFavoriteSaga);
  yield takeLatest(DELETE_SNIPPET, deleteSnippetSaga);
}
