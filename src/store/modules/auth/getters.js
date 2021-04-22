export default {
  assignableUsers: (state) => {
    const users = Object.values(state.users);
    users.unshift({ name: 'Unassigned', sub: 'null', email: null });
    return users;
  },
  currentUser: (state) => ({ ...state.userInfo, id: state.userInfo.sub }),
  user: (state) => (id) => {
    const user = state.users[id];
    if (user) {
      return user;
    }
    return undefined;
  },
  users: (state, getters) => Object.keys(state.users).map(getters.user),
};
