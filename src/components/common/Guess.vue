<template>
  <div>
    <div v-if="fobbit.answers">
      <p v-if="fobbit.have_guessed">Your guess was submitted</p>
      <v-form v-else @submit.prevent="guess" id="guess">
        <v-list flat>
          <v-list-item-group v-model="answer" color="primary">
            <v-list-item
              v-for="answer in fobbit.answers"
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
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

export default {
  name: 'Guess',
  props: {
    fobbit: undefined,
  },
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
    }),
  },
  methods: {
    guess() {
      this.$store.dispatch(
        'guess',
        {
          id: this.fobbit.id,
          answer: this.fobbit.answers[this.answer].id,
        },
      )
        .then(() => {
          console.log('jalo');
          this.fobbit.have_guessed = true;
        });
    },
  },
};
</script>
