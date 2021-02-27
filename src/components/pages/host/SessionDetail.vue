<template>
<!-- class="xs10 offset-xs1" -->
    <v-layout class="xs10 offset-xs1">
      SessionDetail
      <div v-if="session">
        <h1>
          Session : {{ session.name }}
        </h1>
        <FobbitDetail
          v-if="session.active_fobbit"
          :fobbit="session.active_fobbit"
        />
        <div v-else>
          <h2>
            no active question
          </h2>
        </div>
        <v-btn @click="$store.dispatch('nextQuestion', ({ sessionId }))">
          Next question
        </v-btn>
        <v-btn @click="$store.dispatch('prevQuestion', ({ sessionId }))">
          Prev question
        </v-btn>
        <v-pagination
          v-model="fobbitIndex"
          :length="session.fobbits.length"
          @click="setFobbit"
        ></v-pagination>
      </div>

      <div v-else>
        <h2>no session</h2>
      </div>
    </v-layout>
</template>

<script>
import { mapState } from 'vuex';
import FobbitDetail from './FobbitDetail.vue';

export default {
  name: 'SessionDetail',
  components: {
    FobbitDetail,
  },
  props: {
    sessionId: Number,
  },
  created() {
    this.refresh();
  },
  data() {
    return {
      fobbitIndex: 0,
    };
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
    setFobbit() {
      this.$store.dispatch(
        'setActiveFobbit',
        { session: this.session, fobbitId: this.session.fobbits[this.fobbitIndex] },
      );
    },
    connectToWebSocket() {
    //   if (this.sessionId) {
    //     const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    //     const uri = this.session.websocket;
    //     this.$store.dispatch('connectToWebSocket', { scheme, uri });
    //   }
    },
  },
  watch: {
    session: 'connectToWebSocket',
    fobbitIndex: 'setFobbit',
  },
};
</script>
