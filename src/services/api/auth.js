import axios from 'axios';

const options = {};
const tokenKey = 'fobbage-user';
const prevToken = localStorage.getItem(tokenKey);
if (prevToken) {
  options.Authorization = `JWT ${prevToken}`;
}

const axiosClient = axios.create({
  baseURL: process.env.VUE_APP_FOBBAGESAPI_BACKEND_URL || 'https://fobbage.herokuapp.com/',
  ...options,
});


export default {
  login: credentials => new Promise((resolve, reject) => {
    axiosClient.post('api/token/', credentials)
      .then((resp) => {
        const { token } = resp.data;
        localStorage.setItem(tokenKey, token);
        resolve(resp);
      })
      .catch((err) => {
        // if the request fails, remove any possible user token if possible
        localStorage.removeItem(tokenKey);
        reject(err);
      });
  }),
  logout: () => {
    localStorage.removeItem(tokenKey);
  },
  refresh: token => new Promise((resolve, reject) => {
    axiosClient.post('api/refreshtoken/', { token }, {
      refresh: true,
    })
      .then((resp) => {
        const newToken = resp.data.token;
        localStorage.setItem(tokenKey, newToken);
        resolve(resp);
      })
      .catch((err) => {
        localStorage.removeItem(tokenKey);
        reject(err);
      });
  }),
  register: credentials => new Promise((resolve, reject) => {
    axiosClient.post('api/register', credentials)
      .then((resp) => {
        resolve(resp);
      })
      .catch((err) => {
        reject(err);
      });
  }),
};
