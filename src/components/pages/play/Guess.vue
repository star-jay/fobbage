<template>
  <div>
    <div v-if="fobbit.answers">
      <p v-if="fobbit.have_guessed">
        You have guessed. Time to reward your favorite answer!
      </p>
      <v-list flat>
        <v-list-item
          v-for="(answer, index) in fobbit.answers"
          :key="answer.id"
        >
          <v-list-item-content>
            <v-list-item-title>
                <h3>{{ index }}
                  <v-btn
                    class="mx-1"
                    color="primary"
                    @click="guess(index)"
                    :disabled="fobbit.have_guessed"
                  >
                  Vote!
                </v-btn>
                <v-btn
                  class="mx-1"
                  color="accent"
                  @click="like(index)"
                  :disabled="fobbit.have_liked"
                >
                  Like &#128077;
                </v-btn>
                </h3>

            </v-list-item-title>
          </v-list-item-content>
          <!-- U+1F44D unicode is  -->
          </v-list-item>
        </v-list>
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
    guess(index) {
      this.$store.dispatch('guess', {
        id: this.fobbit.id,
        answer: this.fobbit.answers[index].id,
      })
        .then(() => {
          this.fobbit.have_guessed = true;
        });
    },
    like(index) {
      this.$store.dispatch('like', {
        id: this.fobbit.id,
        answer: this.fobbit.answers[index].id,
      })
        .then(() => {
          this.fobbit.have_guessed = true;
        });
    },
  },
};
</script>
