<template>
<!-- class="xs10 offset-xs1" -->
    <v-layout class="xs10 offset-xs1">
      <div v-if="activeSession">
        <h1>
          Quiz : {{ activeSession.title }}
        </h1>
        <div v-if="activeQuestion && activeQuestion.text">
          <h2>
          {{ activeQuestion.text }}
          </h2>

          <Guess v-if="activeQuestion.status===1"/>
          <Bluff v-else-if="activeQuestion.status===0"/>
          <p v-else>
            No action required.
          </p>
        </div>
        <div v-else>
          <h2>
            no active question
          </h2>
        </div>
      </div>

      <div v-else>
        <h2>no active session</h2>
      </div>
    </v-layout>
</template>

<script>
import { mapGetters, mapState } from 'vuex';
import Bluff from '@/components/common/Bluff.vue';
import Guess from '@/components/common/Guess.vue';

export default {
  name: 'Play',
  components: {
    Bluff, Guess,
  },
  props: {
    id: Number,
  },
  created() {
    this.refresh();
  },
  computed: {
    ...mapGetters(['activeSession', 'questionStatus']),
    ...mapState({
      messages: (state) => state.quizes.messages,
      activeQuestion: (state) => state.quizes.activeQuestion,
      activeSessionId: (state) => state.quizes.activeSessionId,
    }),
  },
  methods: {
    refresh() {
      if (this.id) {
        this.$store.dispatch('joinQuiz', { id: this.id });
      }
    },
    connectToWebSocket() {
      if (this.activeSessionId) {
        const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const uri = this.activeSession.websocket;
        this.$store.dispatch('connectToWebSocket', { scheme, uri });
      }
    },
  },
  watch: {
    activeSession: 'connectToWebSocket',
  },
};
</script>
