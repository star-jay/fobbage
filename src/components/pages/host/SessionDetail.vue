<template>
<!-- class="xs10 offset-xs1" -->
    <v-layout class="xs10 offset-xs1">
      <web-socket :sessionId="sessionId"/>
      <div v-if="session">
        <h1>
          Session : {{ session.name }}
        </h1>

        <router-view
          v-if="session.active_fobbit"
          :fobbit="session.active_fobbit">
        </router-view >
         <div v-else>
          <h2>
            no active question
          </h2>
        </div>

        <v-row>
          <v-pagination
            total-visible="10"
            v-model="fobbitIndex"
            :length="session.fobbits.length"
            @click="setFobbit"
          ></v-pagination>
          <v-btn @click="$store.dispatch('nextQuestion', ({ sessionId }))">
            Next question
          </v-btn>
        </v-row>
        <v-btn :to="{ name: 'scores' }">
          Scores
        </v-btn>
      </div>
      <div v-else>
        <h2>no session</h2>
      </div>
    </v-layout>
</template>

<script>
import { mapState } from 'vuex';
import WebSocket from '@/components/common/WebSocket.vue';

export default {
  name: 'SessionDetail',
  components: {
    WebSocket,
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
  },
  watch: {
    fobbitIndex: 'setFobbit',
  },
};
</script>
