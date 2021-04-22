import Vue from 'vue';
import * as types from './mutation-types';

export default {
  [types.USERINFO_SUCCESS]: (state, userinfo) => {
    state.userInfo = userinfo;
  },
  [types.USERINFO_ERROR]: (state) => {
    state.userInfo = undefined;
  },

  [types.USER_SUCCESS]: (state, { user }) => {
    Vue.set(state.users, user.sub, user);
  },
  [types.USERS_ERROR]: (state, { error }) => {
    state.lastError = error;
  },
  [types.USERS_SUCCESS]: (state, { users }) => {
    state.users = users;
  },

  [types.AUTH_REQUEST_SUCCESS]: () => {
    // state.userInfo = userinfo;
  },
  [types.AUTH_REQUEST_ERROR]: () => {
    // state.userInfo = undefined;
  },
};
