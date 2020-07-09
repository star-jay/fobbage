import axios from 'axios';

const baseURL = process.env.VUE_APP_API_BACKEND_URL || 'http://localhost:8000/';

const client = axios.create({
  baseURL,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    // eslint-disable-next-line
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const clearTokens = (error) => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  // router.push({ name: 'login' }).catch(() => {});
  throw error;
};

const tokenErrorInterceptor = async (error) => {
  // Throw any error that is not due to authentication and
  // handle it by other handlers.
  if (error.response.status !== 401) {
    throw error;
  }

  // If the token was invalid, try to get a new one by using the refresh token.
  if (error.response.data.code === 'token_not_valid') {
    const resp = await axios.post(`${baseURL}refreshtoken/`, {
      refresh: localStorage.getItem('refreshToken'),
    })
      .then((response) => {
        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
        const { config } = error;
        config.headers.Authorization = `Bearer ${response.data.access}`;
        return axios.request(config);
      })
      .catch((refreshError) => {
        // If still not authenticated after sending the refresh token,
        // clear the tokens, the user must reauthenticate.
        if (refreshError.response.status === 401) {
          clearTokens(refreshError);
        } else {
          throw refreshError;
        }
      });
    return resp;
  }

  // If none of the conditions was met, this a 401 error that was
  // raised for some other reason than an bad or expired token.
  // e.g. unexisting user. So throw the error so it can be handled upstream.
  throw error;
};

client.interceptors.response.use(
  undefined,
  tokenErrorInterceptor,
);

export default client;
