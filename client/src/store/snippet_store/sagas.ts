import { call, put, takeEvery } from "redux-saga/effects";
// import { ApolloClient, NormalizedCacheObject } from "@apollo/client";
import {
  ADD_SNIPPET,
  FETCH_SNIPPETS,
  setSnippets,
  setAddSnippetStatus,
  FETCH_SNIPPET,
  setSnippet,
  setFetchSnippetStatus,
} from "./actions";
import { GET_SNIPPETS, GET_SNIPPET } from "../../graphql/snippets/queries";
import { ADD_SNIPPET as ADD_SNIPPET_MUT } from "../../graphql/snippets/mutations";
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
    const { id } = action.payload;
    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_SNIPPET,
      variables: { id },
    });
    // Dispatch an action to set the single user in the state
    if (data.getSnippet) {
      yield put(setSnippet(data.getSnippet));
      yield put(setFetchSnippetStatus("success"));
    } else {
      yield put(setFetchSnippetStatus("not_found")); // or whatever status makes sense
    }
  } catch (error) {
    console.error("Fetch user failed:", error);
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

export default function* rootSaga() {
  yield takeEvery(FETCH_SNIPPETS, fetchSnippetsSaga);
  yield takeEvery(FETCH_SNIPPET, fetchSnippetSaga);
  yield takeEvery(ADD_SNIPPET, addSnippetSaga);
}
