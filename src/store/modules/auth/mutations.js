import moment from 'moment';
import * as types from '@/store/mutation-types';

export default {
  [types.AUTH_REQUEST]: (state) => {
    state.status = 'loading';
  },
  [types.AUTH_SUCCESS]: (state, { token, user }) => {
    state.status = 'success';
    state.token = token;
    state.user = user;
  },
  [types.AUTH_REGISTERED]: (state) => {
    state.status = '';
    state.token = '';
    state.user = null;
  },
  [types.AUTH_ERROR]: (state) => {
    state.status = 'error';
    state.token = undefined;
  },
  [types.AUTH_LOGOUT]: (state) => {
    state.status = '';
    state.token = '';
    state.user = null;
  },
  [types.AUTH_REFRESH]: (state, { token, user }) => {
    state.status = 'success';
    state.token = token;
    state.user = user;
    state.nextRefresh = moment().add(1500, 'minutes');
  },
};
