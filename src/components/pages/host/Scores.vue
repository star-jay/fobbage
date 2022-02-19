<template>
  <div>
    <div v-if="fobbit.score_sheets">
      <Score :score="fobbit.score_sheets[scoreIndex-1]"/>
      <v-btn :to="{ name: 'scoreboard' }">
        Scoreboard
      </v-btn>
      <v-pagination
        small
        v-model="scoreIndex"
        :length="fobbit.score_sheets.length"
      ></v-pagination>
    </div>
    <div v-else>
      This question has no scores.
    </div>
    <v-btn @click="$router.push({ name: 'fobbit-detail' })">
      Go back
    </v-btn>
  </div>
</template>

<script>
import Score from './Score.vue';

export default {
  name: 'Scores',
  components: {
    Score,
  },
  props: {
    fobbit: undefined,
  },
  data() {
    return {
      scoreIndex: 1,
    };
  },
  methods: {
    resetIndex() {
      this.scoreIndex = 1;
    },
  },
  watch: {
    fobbit: 'resetIndex',
  },

};
</script>
