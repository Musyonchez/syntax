import { call, put, takeEvery } from "redux-saga/effects";
import {
  ADD_SNIPPET,
  FETCH_SNIPPETS,
  setSnippets,
  setAddSnippetStatus,
  FETCH_SNIPPET,
  setSnippet,
  setFetchSnippetStatus,
  ADD_FAVORITE,
  setAddFavoriteStatus,
  setSnippets as setSnippetsAfterFavorite, // reuse to update group favorites
  setSnippet as setSnippetAfterFavorite,   // reuse to update single snippet favorite
} from "./actions";
import { GET_SNIPPETS, GET_SNIPPET } from "../../graphql/snippets/queries";
import { ADD_SNIPPET as ADD_SNIPPET_MUT } from "../../graphql/snippets/mutations";
import { ADD_FAVORITE as ADD_FAVORITE_MUT } from "../../graphql/snippets/mutations"; // <-- you'll create this mutation
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
      console.log(id,ifmask,difficulty,data.getSnippet)
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
    console.log("in addfavorites")

    const { id, type = "single" } = action.payload;

    const { data } = yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_FAVORITE_MUT,
      variables: { id, type },
    });

    // data.addFavorite returns either an array of snippets (group) or single snippet array
    if (type === "group") {
      yield put(setSnippetsAfterFavorite(data.addFavorite));
    } else {
      yield put(setSnippetAfterFavorite(data.addFavorite[0])); // single snippet array
    }

    yield put(setAddFavoriteStatus("success"));
  } catch (error) {
    console.error("Add favorite failed:", error);
    yield put(setAddFavoriteStatus("error"));
  }
}

export default function* rootSaga() {
  yield takeEvery(FETCH_SNIPPETS, fetchSnippetsSaga);
  yield takeEvery(FETCH_SNIPPET, fetchSnippetSaga);
  yield takeEvery(ADD_SNIPPET, addSnippetSaga);
  yield takeEvery(ADD_FAVORITE, addFavoriteSaga); 
}
