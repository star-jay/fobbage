<template>
  <div v-if="session" class="ma-8">
    <web-socket :session="session"/>
    <h2>
      {{ session.name }}
    </h2>

    <router-view
      v-if="session.active_fobbit"
      :fobbit="session.active_fobbit"
      :session="session">
    </router-view >

    <div v-else>
      <h3>
        no active question
      </h3>
      <v-btn @click="$store.dispatch('nextQuestion', ({ sessionId }))">
        Next question
      </v-btn>
    </div>
    <Pagination :session="session"/>
  </div>
  <!-- <div v-else>
    <h2>no session, refresh</h2>
  </div> -->
</template>

<script>
import { mapState } from 'vuex';
import WebSocket from '@/components/common/WebSocket.vue';
import Pagination from './Pagination.vue';


export default {
  name: 'SessionDetail',
  components: {
    WebSocket,
    Pagination,
  },
  props: {
    sessionId: Number,
  },
  created() {
    this.refresh();
  },
  data() {
    return {
      fobbitIndex: 1,
    };
  },
  computed: {
    ...mapState({
      messages: state => state.quizes.messages,
    }),
    session() {
      return this.$store.getters.session(this.sessionId);
    },
    calculatedIndex() {
      if (this.session && this.session.fobbits) {
        return this.session.fobbits.findIndex(id => id === this.session.active_fobbit.id) + 1;
      }
      return 1;
    },
  },
  methods: {
    refresh() {
      if (this.sessionId) {
        this.$store.dispatch('retrieveSession', { id: this.sessionId });
      }
    },
    setFobbit(index) {
      this.$store.dispatch(
        'setActiveFobbit',
        { session: this.session, fobbitId: this.session.fobbits[index - 1] },
      );
    },
    updateFobbitIndex() {
      this.fobbitIndex = this.calculatedIndex;
    },
  },
  watch: {
    calculatedIndex: 'updateFobbitIndex',
  },
};
</script>
