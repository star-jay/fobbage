<template>
  <div>
    <ul>
      <li v-for="message in messages" v-bind:key="message.id">
        {{ message }}
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  data() {
    return {
      messages: [
        {
          id: 1,
        },
      ],
    };
  },
  created() {
    setTimeout(this.connectToWebSocket, 1000);
    // this.connectToWebSocket()
  },
  methods: {
    connectToWebSocket() {
      const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
      const chatSocket = `${wsScheme}://${window.location.host}/chat${window.location.pathname}`;

      const websocket = new WebSocket(chatSocket);
      websocket.onopen = this.onOpen;
      websocket.onclose = this.onClose;
      websocket.onmessage = this.onMessage;
      websocket.onerror = this.onError;
    },
    onOpen(event) {
      console.log('Connection opened.', event.data);
    },
    onClose(event) {
      console.log('Connection closed.', event.data);
      // Try and Reconnect after five seconds
      // setTimeout(this.connectToWebSocket, 5000)
    },
    onMessage(event) {
      console.log('new message');
      const message = JSON.parse(event.data);
      this.messages.push(message);
    },
    onError(event) {
      console.log('An error occured:', event.data);
    },
  },
};
</script>
