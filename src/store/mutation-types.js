// After sending auth details
export const AUTH_REQUEST = 'AUTH_REQUEST';
// Successful authentication. Takes token as argument
export const AUTH_SUCCESS = 'AUTH_SUCCESS';
// Error when authenticating
export const AUTH_ERROR = 'AUTH_ERROR';
// After logging user out
export const AUTH_LOGOUT = 'AUTH_LOGOUT';
// After receiving a refreshed token
export const AUTH_REFRESH = 'AUTH_REFRESH';
export const AUTH_REGISTERED = 'AUTH_REGISTERED';


// Start loading QUIZES
export const QUIZES_REQUEST = 'QUIZES_REQUEST';
// QUIZES successfully loaded
export const QUIZES_SUCCESS = 'QUIZES_SUCCESS';
// Problem loading QUIZES
export const QUIZES_ERROR = 'QUIZES_ERROR';

export const QUIZES_JOIN = 'QUIZES_JOIN';

export const BLUFF_REQUEST = 'BLUFF_REQUEST';
export const BLUFF_SUCCESS = 'BLUFF_SUCCESS';
export const BLUFF_ERROR = 'BLUFF_ERROR';

export const GUESS_REQUEST = 'GUESS_REQUEST';
export const GUESS_SUCCESS = 'GUESS_SUCCESS';
export const GUESS_ERROR = 'GUESS_ERROR';

// Socket
export const SOCKET_MESSAGE = 'SOCKET_MESSAGE';
export const SOCKET_ERROR = 'SOCKET_ERROR';
export const SOCKET_OPEN = 'SOCKET_OPEN';
export const SOCKET_CLOSE = 'SOCKET_CLOSE';
export const SOCKET_SET = 'SOCKET_SET';

export const ACTIVE_QUESTION_SUCCES = 'ACTIVE_QUESTION_SUCCES';
