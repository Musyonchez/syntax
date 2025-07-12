import { call, put, takeEvery } from "redux-saga/effects";
import {
  FETCH_USERS,
  ADD_USER,
  FETCH_USER,
  setUsers,
  setUser,
  setAddUserStatus,
} from "./actions";
import { GET_USERS, GET_USER } from "../../graphql/users/queries";
import { ADD_USER as ADD_USER_MUT } from "../../graphql/users/mutation";
import apolloClient from "../../apollo/client";

// Saga to fetch all users
function* fetchUsersSaga() {
  try {
    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_USERS,
    });
    yield put(setUsers(data.getUsers)); // Assuming getUsers is the query field
  } catch (error) {
    console.error("Fetch users failed:", error);
  }
}

// Saga to fetch a single user
function* fetchUserSaga(action: any) {
  try {
    const { email } = action.payload;
    const { data } = yield call([apolloClient, apolloClient.query], {
      query: GET_USER,
      variables: { email }, // ✅ Now it's correct
    });
    // Dispatch an action to set the single user in the state
    if (data.getUser) {
      yield put(setUser(data.getUser));
    // } else {
    //   yield put(setAddUserStatus("not_found")); // or whatever status makes sense
    }
      } catch (error) {
    console.error("Fetch user failed:", error);
  }
}

// Saga to add a user
function* addUserSaga(action: any) {
  try {
    yield put(setAddUserStatus("loading"));

    const { data } = yield call([apolloClient, apolloClient.mutate], {
      mutation: ADD_USER_MUT,
      variables: action.payload,
    });

    // Dispatch the added user to the store (assuming mutation field is `addUser`)
    yield put(setUser(data.addUser));

    // Optional: You can still call fetchUsersSaga to refresh the user list
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
  yield takeEvery(FETCH_USER, fetchUserSaga); // If needed, for fetching a single user
}
