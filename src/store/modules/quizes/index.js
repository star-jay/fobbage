import actions from './actions';
import mutations from './mutations';
import getters from './getters';

export default {
  state: {
    loading: false,
    quizes: [],
    sessions: {},
    error: '',
    bluff: undefined,
    guess: undefined,
    scoreBoard: undefined,
  },
  mutations,
  getters,
  actions,
};
