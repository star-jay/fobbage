import jwtDecode from 'jwt-decode';

import actions from './actions';
import mutations from './mutations';
import getters from './getters';

const getUser = () => {
  const token = localStorage.getItem('fobbage-user') || null;
  let user = null;
  if (token) {
    user = jwtDecode(token);
  }
  return user;
};


export default {
  state: {
    status: '',
    token: localStorage.getItem('fobbage-user') || '',
    user: getUser(),
    nextRefresh: undefined,
  },
  mutations,
  getters,
  actions,
};
