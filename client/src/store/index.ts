import { combineReducers, createStore, applyMiddleware } from "redux";
import createSagaMiddleware from "redux-saga";
import { snippetReducer, snippetSaga } from "./snippet_store";
import { userReducer, userSaga } from "./user_store";
import { all } from "redux-saga/effects";

// Combine reducers
const rootReducer = combineReducers({
  snippet: snippetReducer,
  user: userReducer,
});

// Root saga
function* rootSaga() {
  yield all([snippetSaga(), userSaga()]);
}

// Create the saga middleware
const sagaMiddleware = createSagaMiddleware();

// Create the Redux store
const store = createStore(rootReducer, applyMiddleware(sagaMiddleware));

// Run the root saga
sagaMiddleware.run(rootSaga);

// Export types and store
export type RootState = ReturnType<typeof rootReducer>;
export default store;
