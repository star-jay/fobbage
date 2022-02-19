import {
  quizesAPI,
  bluffsAPI,
  guessAPI,
  // active_fobbitsAPI,
  sessionsAPI,
  fobbitsAPI,
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
  joinSession: ({ commit }, { id }) => {
    sessionsAPI.join(id);
    commit('QUIZES_JOIN', { id });
  },

  bluff: ({ commit }, { fobbit, text }) => new Promise(
    (resolve, reject) => {
      bluffsAPI.post({ fobbit, text })
        .then((response) => {
          commit('BLUFF_SUCCESS', { bluff: response.data });
          resolve(response);
        })
        .catch((error) => {
          commit('BLUFF_ERROR');
          reject(error);
        });
    },
  ),

  editBluff: ({ commit }, { bluff }) => new Promise(
    (resolve, reject) => {
      bluffsAPI.patch(bluff.id, bluff)
        .then((response) => {
          commit('BLUFF_SUCCESS', { bluff: response.data });
          resolve(response);
        })
        .catch((error) => {
          commit('BLUFF_ERROR');
          reject(error);
        });
    },
  ),

  guess: ({ commit }, { fobbit, answer }) => new Promise(
    (resolve, reject) => {
      guessAPI.post({ fobbit, answer })
        .then((response) => {
          commit('GUESS_SUCCESS', { guess: response.data });
          resolve(response);
        })
        .catch((error) => {
          commit('GUESS_ERROR');
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
    if ('session_id' in message) {
      dispatch('retrieveSession', { id: message.session_id });
      // setTimeout(() => {
      //   dispatch('newactive_fobbit');
      // }, 200);
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
          resolve(response.data);
        })
        .catch((error) => {
          commit('SESSIONS_ERROR');
          reject(error);
        });
    },
  ),

  createSession: ({ commit }, { name, settings, quiz }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.post({ name, quiz, settings })
        .then((response) => {
          const session = response.data;
          commit('SESSIONS_SUCCESS', [session]);
          resolve(session);
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

  newRound: ({ commit }, { sessionId, numberOfQuestions, multiplier }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.newRound(sessionId, { number_of_questions: numberOfQuestions, multiplier })
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

  setActiveFobbit: ({ commit }, { session, fobbitId }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.setActiveFobbit(session.id, { active_fobbit: fobbitId })
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

  finishFobbit: ({ commit }, { fobbit }) => new Promise(
    (resolve, reject) => {
      fobbitsAPI.finish(fobbit.id)
        .then((response) => {
          commit('FOBBIT_SUCCESS', [response.data]);
          resolve(response);
        })
        .catch((error) => {
          commit('FOBBIT_ERROR');
          reject(error);
        });
    },
  ),

  resetFobbit: ({ commit }, { fobbit }) => new Promise(
    (resolve, reject) => {
      fobbitsAPI.reset(fobbit.id)
        .then((response) => {
          commit('FOBBIT_SUCCESS', [response.data]);
          resolve(response);
        })
        .catch((error) => {
          commit('FOBBIT_ERROR');
          reject(error);
        });
    },
  ),

  generateAnswersForFobbit: ({ commit }, { fobbit }) => new Promise(
    (resolve, reject) => {
      fobbitsAPI.generateAnswers(fobbit.id)
        .then((response) => {
          commit('FOBBIT_SUCCESS', [response.data]);
          resolve(response);
        })
        .catch((error) => {
          commit('FOBBIT_ERROR');
          reject(error);
        });
    },
  ),

  retrieveScoreBoard: ({ commit }, { id }) => new Promise(
    (resolve, reject) => {
      sessionsAPI.getScoreBoard(id)
        .then((response) => {
          commit('SCOREBOARD_SUCCESS', response.data);
          resolve(response);
        })
        .catch((error) => {
          commit('SCOREBOARD_ERROR');
          reject(error);
        });
    },
  ),
};
