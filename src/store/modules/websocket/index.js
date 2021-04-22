import actions from './actions';
import getters from './getters';
import mutations from './mutations';

export default {
  actions,
  getters,
  mutations,
  state: {
    websocket: undefined,
    messages: [],
    connected: false,
  },
};
