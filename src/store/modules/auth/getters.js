export default {
  authLoading: state => state.status === 'loading',
  isAuthenticated: state => !!state.token,
  refreshRequired: state => (currentTime) => {
    if (!state.token) {
      return false;
    }
    if (state.nextRefresh === undefined) {
      return true;
    }
    return state.nextRefresh.diff(currentTime) < 0;
  },
};
