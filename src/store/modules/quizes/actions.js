import {
  quizesAPI,
  bluffsAPI,
  guessAPI,
  activeQuestionsAPI,
  sessionsAPI,
} from '@/services/api';

export default {
  getQuizList: ({ commit }) => {
    commit('QUIZES_REQUEST');
    return new Promise((resolve, reject) => {
      quizesAPI.get()
        .then((response) => {
          const quizes = response.data;
          commit('QUIZES_SUCCESS', quizes);
          resolve(response);
        })
        .catch((error) => {
          commit('QUIZES_ERROR');
          reject(error);
        });
    });
  },
  joinQuiz: ({ commit, dispatch }, { id }) => {
    commit('QUIZES_JOIN', { id });
    dispatch('newActiveQuestion', { id });
  },
  newActiveQuestion: ({ state, commit }) => new Promise((resolve, reject) => {
    // set active question to zero
    activeQuestionsAPI.get(state.activeQuizId)
      .then((response) => {
        const activeQuestion = response.data;
        commit('ACTIVE_QUESTION_SUCCES', { activeQuestion });
        resolve(response);
      })
      .catch((error) => {
        commit('QUIZES_ERROR');
        reject(error);
      });
  }),
  bluff: ({ state, commit, dispatch }, { text }) => new Promise(
    (resolve, reject) => {
      bluffsAPI.post({ fobbit: state.activeQuestion.id, text })
        .then((response) => {
          commit('BLUFF_SUCCESS', text);
          dispatch('newActiveQuestion');
          resolve(response);
        })
        .catch((error) => {
          commit('BLUFF_ERROR');
          reject(error);
        });
    },
  ),
  sendMessage({ state }, { message }) {
    if (state.websocket) {
      state.websocket.send(JSON.stringify({
        message,
      }));
    }
  },
  sendAnswer({ state }, { answer }) {
    if (state.websocket) {
      state.websocket.send(JSON.stringify({
        answer,
      }));
    }
  },
  createGuess: ({ commit, dispatch }, { id, guess }) => new Promise((resolve, reject) => {
    guessAPI.post({ question: id, answer: guess })
      .then((response) => {
        commit('GUESS_SUCCESS', guess);
        dispatch('newActiveQuestion');
        resolve(response);
      })
      .catch((error) => {
        commit('GUESS_ERROR');
        reject(error);
      });
  }),
  newMessage({ dispatch }, { message }) {
    // toodo: get quiz id from message and query new active question
    if ('quiz_id' in message) {
      setTimeout(() => {
        dispatch('newActiveQuestion');
      }, 200);
    }
  },

  listSessions: ({ commit }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.get()
        .then((response) => {
          commit('SESSIONS_SUCCESS', response.data);
          resolve(response);
        })
        .catch((error) => {
          commit('SESSIONS_ERROR');
          reject(error);
        });
    },
  ),
};
