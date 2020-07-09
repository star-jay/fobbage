import Auth from '@/services/auth';

import {
  AUTH_SUCCESS,
  AUTH_ERROR,
  USERINFO_SUCCESS,
  USERINFO_ERROR,
  USERS_SUCCESS,
  USERS_ERROR,
  USER_SUCCESS,
} from './mutation-types';

export default {
  async login({ commit }, credentials) {
    console.log(Auth.tokens);
    return Auth.simpleToken.post(credentials)
      .then((response) => {
        commit(AUTH_SUCCESS);
        localStorage.setItem('accessToken', response.data.token);
        localStorage.setItem('refreshToken', response.data.refresh);
        return response.data;
      })
      .catch((error) => {
        commit(AUTH_ERROR, { error });
        throw error;
      });
  },
  async getUserinfo({ commit }) {
    Auth.userinfo.get()
      .then((response) => {
        commit(USERINFO_SUCCESS, response.data);
      })
      .catch((error) => {
        commit(USERINFO_ERROR, { error });
        throw error;
      });
  },
  async listUsers({ commit }) {
    return Auth.users.get()
      .then((response) => {
        const users = {};
        response.data.forEach((user) => {
          users[user.sub] = user;
        });
        commit(USERS_SUCCESS, { users });
        return response.data;
      })
      .catch((error) => {
        commit(USERS_ERROR, { error });
        throw error;
      });
  },
  async retrieveUser({ commit }, id) {
    Auth.users.get(id)
      .then((response) => {
        commit(USER_SUCCESS, { user: response.data });
        return response.data;
      })
      .catch((error) => {
        commit(USERS_ERROR, { error });
        throw error;
      });
  },
  async logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },
};
