<template>
  <div>
    Scoreboard
    <v-list flat>
      <v-list-item
        v-for="score in $store.state.quizes.scoreBoard"
        :key="score.player.id"
      >
        <v-list-item-content>
          <v-col>{{ score.player.username }}</v-col>
          <v-col> {{ score.score }} </v-col>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-btn @click="nextQuestion">
      Back
    </v-btn>
  </div>

</template>

<script>

export default {
  name: 'Scoreboard',
  components: {
  },
  props: {
    session: undefined,
  },
  data() {
    return {
    };
  },
  created() {
    this.$store.dispatch('retrieveScoreBoard', { id: this.session.id });
  },
  methods: {
    nextQuestion() {
      // this.$store.dispatch('nextQuestion', ({ sessionId: this.session.id })).then(() => {
      this.$router.push({ name: 'session-detail' });
      // });
    },
  },
  watch: {
    // fobbit: 'resetIndex',
  },

};
</script>
