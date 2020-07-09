<template>
  <div>
    <div v-if="activeQuestion.answers">
      <p v-if="activeQuestion.have_guessed">Your guess was submitted</p>
      <v-form v-else @submit.prevent="guess" id="guess">
        <v-list flat>
          <v-list-item-group v-model="answer" color="primary">
            <v-list-item
              v-for="answer in activeQuestion.answers"
              :key="answer.id"
            >
              <template v-slot:default="{ active }">
                <v-list-item-action>
                  <v-checkbox v-model="active"></v-checkbox>
                </v-list-item-action>
                <v-list-item-content>
                <v-list-item-title v-text="answer.order">
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <v-btn type="submit" color="primary" form="guess">Guess</v-btn>
      </v-form>
    </div>
    <div v-else>
      <p>
        No action required.
      </p>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

export default {
  name: 'Guess',
  data() {
    return {
      errors: [],
      answer: undefined,
      order: undefined,
    };
  },
  computed: {
    ...mapGetters(['activeQuiz']),
    ...mapState({
      activeQuestion: state => state.quizes.activeQuestion,
    }),
  },
  methods: {
    guess() {
      this.$store.dispatch(
        'guess',
        {
          id: this.activeQuestion.id,
          guess: this.activeQuestion.answers[this.answer].id,
        },
      );
    },
  },
};
</script>
