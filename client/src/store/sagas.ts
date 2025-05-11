import { call, put, takeEvery } from "redux-saga/effects";
import { ApolloClient, NormalizedCacheObject } from "@apollo/client";
import { ADD_SNIPPET, FETCH_SNIPPETS, setSnippets } from "./actions";
import { GET_SNIPPETS } from "../graphql/queries";
import { ADD_SNIPPET as ADD_SNIPPET_MUT } from "../graphql/mutations";
import apolloClient from "../apollo/client";

function* fetchSnippetsSaga() {
  const { data } = yield call([apolloClient, apolloClient.query], {
    query: GET_SNIPPETS,
  });
  yield put(setSnippets(data.getSnippets));
}

function* addSnippetSaga(action: any) {
    yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_SNIPPET_MUT,
      variables: {
        title: action.payload.title,
        content: action.payload.content,
        language: action.payload.language,
        createdAt: action.payload.createdAt,
        userId: action.payload.userId,
      },
      
    });
    console.log(action.payload);
    yield call(fetchSnippetsSaga); // Refresh list after adding
  }
  

export default function* rootSaga() {
  yield takeEvery(FETCH_SNIPPETS, fetchSnippetsSaga);
  yield takeEvery(ADD_SNIPPET, addSnippetSaga);
}
