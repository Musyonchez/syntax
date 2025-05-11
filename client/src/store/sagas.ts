import { call, put, takeEvery } from "redux-saga/effects";
import { ApolloClient, NormalizedCacheObject } from "@apollo/client";
import { ADD_SNIPPET, FETCH_SNIPPETS, setSnippets } from "./actions";
import { GET_SNIPPETS } from "../graphql/queries";
import { setAddSnippetStatus } from "./actions";
import { ADD_SNIPPET as ADD_SNIPPET_MUT } from "../graphql/mutations";
import apolloClient from "../apollo/client";

function* fetchSnippetsSaga() {
  const { data } = yield call([apolloClient, apolloClient.query], {
    query: GET_SNIPPETS,
  });
  yield put(setSnippets(data.getSnippets));
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
  yield takeEvery(ADD_SNIPPET, addSnippetSaga);
}
