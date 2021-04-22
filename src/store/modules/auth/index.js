import actions from './actions';
import mutations from './mutations';
import getters from './getters';

function initialState() {
  return {
    userInfo: {},
    users: {},
  };
}

export default {
  state: initialState,
  actions,
  mutations,
  getters,
};
