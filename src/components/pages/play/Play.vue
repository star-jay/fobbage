<template>
<!-- class="xs10 offset-xs1" -->
    <v-layout class="xs10 offset-xs1">
      <div v-if="session">
        <h1>
          Session : {{ session.name }}
        </h1>
        <div v-if="session.active_fobbit">
          <h2>
          {{ session.active_fobbit.question.text }}
          </h2>

          <Guess v-if="session.active_fobbit.status===1"/>
          <Bluff v-else-if="session.active_fobbit.status===0"/>
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
import { mapState } from 'vuex';
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
    ...mapState({
      messages: (state) => state.quizes.messages,
    }),
    session() {
      return this.$store.state.quizes.sessions[this.id];
    },
  },
  methods: {
    refresh() {
      if (this.id) {
        console.log(this.id);
        // this.$store.dispatch('retrieve?Session', { id: this.id });
        this.$store.dispatch('joinQuiz', { id: this.id });
      }
    },
    connectToWebSocket() {
      // if (this.sessionId) {
      //   const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
      //   const uri = this.session.websocket;
      //   this.$store.dispatch('connectToWebSocket', { scheme, uri });
      // }
    },
  },
  watch: {
    session: 'connectToWebSocket',
  },
};
</script>
