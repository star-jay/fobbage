import { client, tokenErrorInterceptor } from './authClient';
import tokens from './tokens';
import userinfo from './userinfo';
import users from './users';

export default {
  tokens,
  userinfo,
  users,
  register: (form) => client.post('registration/', form),
  emailVerification: (verificationKey) => client.get(`emailverification/${verificationKey}/`),
  passwordReset: (data) => client.post('passwordreset/', data),
  passwordResetConfirmation: (uid, token, data) => client.post(`passwordreset-confirmation/${uid}/${token}/`, data),
  acceptTerms: (data) => client.patch('accept-terms/', data),
  passwordChange: (data) => client.patch('passwordchange/', data),
  profileChange: (data) => client.patch('profilechange/', data),
  tokenErrorInterceptor,
};
