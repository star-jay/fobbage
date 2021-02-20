import {
  quizesAPI,
  bluffsAPI,
  guessAPI,
  // active_fobbitsAPI,
  sessionsAPI,
} from '@/services/api';

export default {
  listQuizes: ({ commit }) => {
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
    dispatch('retrieveSession', { id });
  },
  // newactive_fobbit: ({ state, commit }) => new Promise((resolve, reject) => {
  //   // set active question to zero
  //   active_fobbitsAPI.get(state.sessionId)
  //     .then((response) => {
  //       const active_fobbit = response.data;
  //       commit('ACTIVE_QUESTION_SUCCES', { active_fobbit });
  //       resolve(response);
  //     })
  //     .catch((error) => {
  //       commit('QUIZES_ERROR');
  //       reject(error);
  //     });
  // }),
  bluff: ({ state, commit, dispatch }, { text }) => new Promise(
    (resolve, reject) => {
      bluffsAPI.post({ fobbit: state.active_fobbit.id, text })
        .then((response) => {
          commit('BLUFF_SUCCESS', text);
          dispatch('newactive_fobbit');
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
        dispatch('newactive_fobbit');
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
        dispatch('newactive_fobbit');
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

  retrieveSession: ({ commit }, { id }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.get(id)
        .then((response) => {
          commit('SESSIONS_SUCCESS', [response.data]);
          resolve(response);
        })
        .catch((error) => {
          commit('SESSIONS_ERROR');
          reject(error);
        });
    },
  ),

  createSession: ({ commit }, { name, quiz }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.post({ name, quiz })
        .then((response) => {
          commit('SESSIONS_SUCCESS', [response.data]);
          resolve(response);
        })
        .catch((error) => {
          commit('SESSIONS_ERROR');
          reject(error);
        });
    },
  ),

  nextQuestion: ({ commit }, { sessionId }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.nextQuestion(sessionId)
        .then((response) => {
          commit('SESSIONS_SUCCESS', [response.data]);
          resolve(response);
        })
        .catch((error) => {
          commit('SESSIONS_ERROR');
          reject(error);
        });
    },
  ),
};
