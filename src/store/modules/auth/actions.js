import { simpleTokenAPI, userInfoAPI } from '@/services/api';

import {
  AUTH_SUCCESS,
  AUTH_ERROR,
  AUTH_REQUEST_SUCCESS,
  AUTH_REQUEST_ERROR,
  USERINFO_SUCCESS,
  USERINFO_ERROR,
} from './mutation-types';

export default {
  async login({ commit }, credentials) {
    return simpleTokenAPI.post(credentials)
      .then((response) => {
        commit(AUTH_SUCCESS);
        localStorage.setItem('accessToken', response.data.token);
        return response.data;
      })
      .catch((error) => {
        commit(AUTH_ERROR, { error });
        throw error;
      });
  },

  async logout() {
    localStorage.removeItem('accessToken');
  },

  async retrieveUserInfo({ commit }) {
    return userInfoAPI.get()
      .then((response) => {
        commit(USERINFO_SUCCESS, response.data);
      })
      .catch((error) => {
        commit(USERINFO_ERROR, { error });
        throw error;
      });
  },

  async register({ commit }, form) {
    return userInfoAPI.post(form)
      .then((response) => {
        commit(AUTH_REQUEST_SUCCESS);
        return response.data;
      })
      .catch((error) => {
        commit(AUTH_REQUEST_ERROR);
        throw error;
      });
  },
};
