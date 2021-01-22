export default {
  activeSession: (state) => state.sessions.find((session) => session.id === state.activeSessionId),
  questionStatus: (state, getters) => {
    if (getters.activeSession && getters.activeSession.active_question) {
      return getters.activeSession.active_question.status;
    }
    return -1;
  },
};
