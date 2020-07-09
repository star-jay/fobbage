// import Vue from 'vue';
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
    state.activeQuizId = id;
    state.bluff = '';
  },
  [types.BLUFF_REQUEST]: (state) => {
    state.loading = true;
  },
  [types.BLUFF_SUCCESS]: (state, bluff) => {
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
  [types.ACTIVE_QUESTION_SUCCES]: (state, { activeQuestion }) => {
    state.activeQuestion = activeQuestion;
    state.error = 'There was a problem!';
  },
};
