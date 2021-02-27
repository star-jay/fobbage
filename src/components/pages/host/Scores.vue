<template>
  <div v-if="fobbit.score_sheets">
    <Score :score="fobbit.score_sheets[scoreIndex-1]"/>
    <v-pagination
      small
      v-model="scoreIndex"
      :length="fobbit.score_sheets.length"
    ></v-pagination>
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

};
</script>
