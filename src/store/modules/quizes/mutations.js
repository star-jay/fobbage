import Vue from 'vue';
import * as types from '@/store/mutation-types';

export default {
  [types.QUIZES_REQUEST]: (state) => {
    state.loading = true;
  },
  [types.QUIZES_SUCCESS]: (state, quizes) => {
    state.quizes = quizes;
    state.loading = false;
  },
  [types.QUIZES_ERROR]: (state) => {
    state.loading = false;
    state.error = 'There was a problem!';
  },
  [types.QUIZES_JOIN]: (state, { id }) => {
    state.sessionId = id;
    state.bluff = '';
  },
  [types.BLUFF_REQUEST]: (state) => {
    state.loading = true;
  },
  [types.BLUFF_SUCCESS]: (state, { bluff }) => {
    state.bluff = bluff;
    state.loading = false;
  },
  [types.BLUFF_ERROR]: (state) => {
    state.loading = false;
    state.error = 'There was a problem!';
  },
  [types.GUESS_REQUEST]: (state) => {
    state.loading = true;
  },
  [types.GUESS_SUCCESS]: (state, { guess }) => {
    state.guess = guess;
    state.loading = false;
  },
  [types.GUESS_ERROR]: (state) => {
    state.loading = false;
    state.error = 'There was a problem!';
  },

  [types.SESSIONS_SUCCESS]: (state, sessions) => {
    sessions.forEach((s) => {
      Vue.set(state.sessions, s.id, s);
    });
  },
  [types.SESSIONS_ERROR]: (state) => {
    state.sessions = [];
  },
  [types.SCOREBOARD_SUCCESS]: (state, scoreBoard) => {
    Vue.set(state, 'scoreBoard', scoreBoard);
  },
  [types.SCOREBOARD_ERROR]: (state) => {
    state.sessions = [];
  },
  [types.LIKE_SUCCESS]: (state, { like }) => {
    state.like = like;
  },
  [types.LIKE_ERROR]: (state) => {
    state.error = 'There was a problem! Liking.';
  },
};
