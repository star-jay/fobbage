<template>
<!-- class="xs10 offset-xs1" -->
    <v-layout class="xs10 offset-xs1">
      SessionDetail
      <div v-if="session">
        <h1>
          Session : {{ session.name }}
        </h1>
        <div v-if="session.active_fobbit">
          <h2>
          {{ session.active_fobbit.question.text }}
          </h2>
        </div>
        <div v-else>
          <h2>
            no active question
          </h2>
        </div>
        <v-btn @click="$store.dispatch('nextQuestion', ({ sessionId }))">
          Next question
        </v-btn>
      </div>

      <div v-else>
        <h2>no session</h2>
      </div>
    </v-layout>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'SessionDetail',
  props: {
    sessionId: Number,
  },
  created() {
    this.refresh();
  },
  computed: {
    ...mapState({
      messages: (state) => state.quizes.messages,
    }),
    session() {
      return this.$store.getters.session(this.sessionId);
    },
  },
  methods: {
    refresh() {
      if (this.sessionId) {
        this.$store.dispatch('retrieveSession', { id: this.sessionId });
      }
    },
    connectToWebSocket() {
      if (this.sessionId) {
        const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const uri = this.session.websocket;
        this.$store.dispatch('connectToWebSocket', { scheme, uri });
      }
    },
  },
  watch: {
    session: 'connectToWebSocket',
  },
};
</script>
