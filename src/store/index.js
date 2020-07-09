import Vue from 'vue';
import Vuex from 'vuex';
import vueMoment from 'vue-moment';

import auth from './modules/auth';
import quizes from './modules/quizes';
import websocket from './modules/websocket';


Vue.use(Vuex);
Vue.use(vueMoment);

export default new Vuex.Store({
  modules: {
    auth,
    quizes,
    websocket,
  },
  getters: {
    isLoading: state => state.quizes.loading,
  },
});
