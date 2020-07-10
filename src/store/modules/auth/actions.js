import { simpleTokenAPI } from '@/services/api';

import {
  AUTH_SUCCESS,
  AUTH_ERROR,
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
};
