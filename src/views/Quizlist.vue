<template>
  <v-list flat>
    <v-subheader>Quizes</v-subheader>
    <v-list-item-group v-model="quizlist" color="primary">
      <v-list-item
        v-for="quiz in quizlist"
        :key="quiz.name"
        :to="'/'+quiz.id"
      >
        <v-list-item-content>
          <v-list-item-title v-text="quiz.title">
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Quizlist',
  computed: {
    ...mapState({
      quizlist: state => state.quizes.quizes,
    }),
  },
  methods: {
    joinQuiz(id) {
      this.$store.dispatch('joinQuiz', { id });
    },
  },
  created() {
    this.$store.dispatch('getQuizList');
  },
};
</script>
