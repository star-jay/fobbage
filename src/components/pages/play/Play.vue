<template>
  <v-layout class="xs10 offset-xs1">
    <div v-if="session">
      <web-socket :session="session"/>
      <h1>
        Session : {{ session.name }}
      </h1>
      <div v-if="session.active_fobbit">
        <h2>
        {{ session.active_fobbit.question.text }}
        </h2>

        <Bluff v-if="session.active_fobbit.status===0"
          :fobbit='session.active_fobbit'
        />

        <Guess v-else-if="session.active_fobbit.status===1"
          :fobbit='session.active_fobbit'
        />
        <p v-else>
          Look at the screen to see your score.
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
import { mapState } from 'vuex';
import Bluff from '@/components/common/Bluff.vue';
import Guess from '@/components/common/Guess.vue';
import WebSocket from '@/components/common/WebSocket.vue';

export default {
  name: 'Play',
  components: {
    Bluff, Guess, WebSocket,
  },
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
        this.$store.dispatch('joinSession', { id: this.sessionId });
      }
    },
  },
  watch: {
  },
};
</script>
