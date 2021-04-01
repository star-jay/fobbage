<template>
  <div/>
</template>
<script>

export default {
  name: 'WebSocket',
  props: {
    session: undefined,
  },
  data() {
    return {
    };
  },
  created() {
    if (this.session) {
      this.connectToWebSocket();
    }
  },
  computed: {
  },
  methods: {
    connectToWebSocket() {
      if (this.session) {
        const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const uri = this.session.websocket;
        this.$store.dispatch('connectToWebSocket', { scheme, uri });
      }
    },
  },
};
</script>
