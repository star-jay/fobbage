export default {
  session: state => id => state.sessions[id],
  // questionStatus: (state, getters) => {
  //   if (getters.session && getters.session.active_question) {
  //     return getters.session.active_question.status;
  //   }
  //   return -1;
  // },
};
