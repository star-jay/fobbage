import axios from 'axios';

const baseURL = process.env.VUE_APP_API_BACKEND_URL || 'http://localhost:8000/';

const client = axios.create({
  baseURL,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    // eslint-disable-next-line
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

const clearTokens = (error) => {
  localStorage.removeItem('accessToken');
  throw error;
};

const tokenErrorInterceptor = async (error) => {
  // Throw any error that is not due to authentication and
  // handle it by other handlers.
  if ([401, 403].includes(error.response.status)) {
    clearTokens(error);
  }
  throw error;
};

client.interceptors.response.use(
  undefined,
  tokenErrorInterceptor,
);

export default client;
