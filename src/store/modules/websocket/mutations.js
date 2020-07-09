import * as types from '@/store/mutation-types';

export default {
  [types.SOCKET_SET]: (state, { websocket }) => {
    state.websocket = websocket;
  },
  [types.SOCKET_OPEN]: (state) => {
    state.connected = true;
  },
  [types.SOCKET_CLOSE]: (state) => {
    state.connected = false;
  },
  [types.SOCKET_MESSAGE]: (state, { event }) => {
    const message = JSON.parse(event.data);
    state.messages.push(message);
  },
  [types.SOCKET_ERROR]: (state, { event }) => {
    const message = JSON.parse(event.data);
    state.error = message;
  },
};
