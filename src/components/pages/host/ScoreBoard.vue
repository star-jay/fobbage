<template>
  <div>
    Scoreboard
    <v-list flat>
      <v-list-item
        v-for="score in scores"
        :key="score.player.id"
      >
        <v-list-item-content>
          <v-col>{{ score.player.username }}</v-col>
          <v-col> {{ score.score }} </v-col>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-btn @click="goBack">
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
    goBack() {
      this.$router.push({ name: 'session-detail' });
    },
  },
  computed: {
    scores() {
      if (this.$store.state.quizes.scoreBoard) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        return this.$store.state.quizes.scoreBoard.sort((a, b) => a.score - b.score);
      }
      return [];
    },
  },
  watch: {
    // fobbit: 'resetIndex',
  },

};
</script>
