<template>
  <div class="hello">
    <h1>
      {{ activeQuiz.active_question.text }}
    </h1>
    <input value="" v-model="my_bluff">
    <button class="button" v-on:click="bluff()">Bluff</button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Bluff',
  data: () => ({
    my_bluff: undefined,
  }),
  computed: {
    ...mapGetters(['activeQuiz']),
  },
  methods: {
    bluff() {
      this.$store.dispatch('bluff', { id: this.$store.getters.activeQuiz.active_question.id, bluff: this.my_bluff });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
