<template>
  <div>
    <div v-if="active_fobbit.answers">
      <p v-if="active_fobbit.have_guessed">Your guess was submitted</p>
      <v-form v-else @submit.prevent="guess" id="guess">
        <v-list flat>
          <v-list-item-group v-model="answer" color="primary">
            <v-list-item
              v-for="answer in active_fobbit.answers"
              :key="answer.id"
            >
              <template v-slot:default="{ active }">
                <v-list-item-action>
                  <v-checkbox :value="active" disabled></v-checkbox>
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
    ...mapGetters(['session']),
    ...mapState({
      active_fobbit: (state) => state.quizes.active_fobbit,
    }),
  },
  methods: {
    guess() {
      this.$store.dispatch(
        'guess',
        {
          id: this.active_fobbit.id,
          guess: this.active_fobbit.answers[this.answer].id,
        },
      );
    },
  },
};
</script>
