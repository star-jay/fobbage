import App from '@/components/layouts/App.vue';
import Vue from 'vue';
import Vuetify from './plugins/vuetify';

import router from './router';
import store from './store';
import 'vuetify/dist/vuetify.min.css';

Vue.config.productionTip = false;

Vue.use(Vuetify);

new Vue({
  router,
  store,
  vuetify: Vuetify,
  render: (h) => h(App),
}).$mount('#app');
