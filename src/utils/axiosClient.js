import moment from 'moment';
import axios from 'axios';
import store from '@/store';
import router from '@/router';


const options = {};

const prevToken = localStorage.getItem('fobbage-token');
if (prevToken) {
  options.Authorization = `JWT ${prevToken}`;
}

const instance = axios.create({
  baseURL: process.env.VUE_APP_FOBBAGESAPI_BACKEND_URL || 'https://fobbage.herokuapp.com/',
  ...options,
});

instance.interceptors.request.use((config) => {
  // If not requesting refresh token...
  if (!config.refresh) {
    // Add authorization in the header
    if (!config.headers.Authorization) {
      const { token } = store.state.auth;
      if (token) {
        // eslint-disable-next-line
        config.headers.Authorization = `JWT ${token}`;
      }
    }
    if (store.getters.refreshRequired(moment())) {
      store.dispatch('refreshToken');
    }
  }
  return config;
});

instance.interceptors.response.use(undefined, err => new Promise(() => {
  // eslint-disable-next-line
  if (err.response && err.response.status === 401 && err.config && !err.config.__isRetryRequest) {
    // if you ever get an unauthenticated, logout the user
    // TODO: attempt refresh token
    store.dispatch('logout');
    instance.defaults.headers.common.Authorization = '';
    router.push({ name: 'login' });
  }
  throw err;
}));


export default instance;
