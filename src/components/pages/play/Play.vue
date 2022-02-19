<template>
  <v-layout class="ma-2">
    <div v-if="session">
      <web-socket :session="session"/>
      <h1>
        Session : {{ session.name }}
      </h1>
      <div v-if="session.active_fobbit">
        <h3>
        {{ session.active_fobbit.question.text }}
        </h3>

        <Bluff v-if="session.active_fobbit.status===0"
          :fobbit='session.active_fobbit'
          :key="session.active_fobbit.id"
        />

        <Guess v-else-if="session.active_fobbit.status===1"
          :fobbit='session.active_fobbit'
          :key="session.active_fobbit.id"
        />
        <p v-else>
          Look at the screen to see your score.
        </p>
      </div>
      <div v-else>
        <h3>
          no active question
        </h3>
      </div>
    </div>
    <div v-else>
      <h3>no active session</h3>
    </div>
  </v-layout>
</template>

<script>
import { mapState } from 'vuex';
import Bluff from '@/components/pages/play/Bluff.vue';
import Guess from '@/components/pages/play/Guess.vue';
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
      messages: state => state.quizes.messages,
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
