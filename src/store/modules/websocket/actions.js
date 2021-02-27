export default {
  connectToWebSocket: ({ state, commit, dispatch }, { scheme, uri }) => {
    const websocket = new WebSocket(`${scheme}://${uri}`);
    websocket.onopen = () => {
      commit('SOCKET_OPEN');
    };
    websocket.onclose = () => {
      commit('SOCKET_CLOSE');
    };
    websocket.onerror = (event) => {
      commit('SOCKET_ERROR', { event });
    };
    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      state.messages.push(message);
      dispatch('newMessage', { message });
    };
    commit('SOCKET_SET', { websocket });
  },
};
