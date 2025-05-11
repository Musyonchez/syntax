import { call, put, takeEvery } from "redux-saga/effects";
import { ApolloClient, NormalizedCacheObject } from "@apollo/client";
import { FETCH_USERS, SET_USERS, setUsers, setAddUserStatus, ADD_USER } from "./actions";
import { GET_USERS, GET_USER } from "../../graphql/users/queries";
import { ADD_USER as ADD_USER_MUT } from "../../graphql/users/mutation";
import apolloClient from "../../apollo/client";

// Saga to fetch all users
function* fetchUsersSaga() {
  try {
    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_USERS,
    });
    yield put(setUsers(data.getUsers));  // Assuming getUsers is the query field
  } catch (error) {
    console.error("Fetch users failed:", error);
  }
}

// Saga to fetch a single user
function* fetchUserSaga(action: any) {
  try {
    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_USER,
      variables: { id: action.payload },  // assuming the user id is in the payload
    });
    // Dispatch an action to set the single user in the state
    yield put({ type: SET_USERS, payload: [data.getUser] });  // Assuming getUser is the query field for one user
  } catch (error) {
    console.error("Fetch user failed:", error);
  }
}

// Saga to add a user
function* addUserSaga(action: any) {
  try {
    yield put(setAddUserStatus("loading"));

    yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_USER_MUT,
      variables: action.payload,
    });

    // After adding, refetch users
    yield call(fetchUsersSaga);
    yield put(setAddUserStatus("success"));
  } catch (error) {
    console.error("Add user failed:", error);
    yield put(setAddUserStatus("error"));
  }
}

export default function* userSaga() {
  yield takeEvery(FETCH_USERS, fetchUsersSaga);
  yield takeEvery(ADD_USER, addUserSaga);
  yield takeEvery("FETCH_USER", fetchUserSaga);  // If needed, for fetching a single user
}
