import jwtDecode from 'jwt-decode';

import authAPI from '@/services/api/auth';

import {
  AUTH_REQUEST,
  AUTH_SUCCESS,
  AUTH_LOGOUT,
  AUTH_ERROR,
  AUTH_REFRESH,
  AUTH_REGISTERED,
} from '@/store/mutation-types';


export default {
  login({ commit }, credentials) {
    commit(AUTH_REQUEST);
    return new Promise((resolve, reject) => {
      authAPI.login(credentials)
        .then((response) => {
          const { token } = response.data;
          const authUser = jwtDecode(token);
          commit(AUTH_SUCCESS, { token, user: authUser });
          resolve(response);
        })
        .catch((error) => {
          commit(AUTH_ERROR);
          authAPI.logout();
          reject(error);
        });
    });
  },
  logout: ({ commit }) => new Promise((resolve) => {
    commit(AUTH_LOGOUT);
    authAPI.logout();
    resolve();
  }),
  refreshToken: ({ commit, state }) => new Promise((resolve, reject) => {
    authAPI.refresh(state.token)
      .then((response) => {
        const { token } = response.data;
        const authUser = jwtDecode(token);
        commit(AUTH_REFRESH, { token, user: authUser });
        resolve(response);
      })
      .catch((error) => {
        commit(AUTH_ERROR);
        authAPI.logout();
        reject(error);
      });
  }),
  register({ commit }, credentials) {
    commit(AUTH_REQUEST);
    return new Promise((resolve, reject) => {
      authAPI.register(credentials)
        .then((response) => {
          commit(AUTH_REGISTERED);
          resolve(response);
        })
        .catch((error) => {
          commit(AUTH_ERROR);
          authAPI.logout();
          reject(error);
        });
    });
  },
};
