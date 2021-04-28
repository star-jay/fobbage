<template>
  <div>
    <div v-if="fobbit.have_bluffed">
      <p>Your bluff was submitted</p>
    </div>
    <div v-else>
    <v-form @submit.prevent="bluff" id="bluff" class="xs10">
      <v-textarea
        v-model="form.bluff"
        name="bluff"
        label="bluff"
        solo
        auto-grow/>
      <v-btn type="submit" color="primary" form="bluff">Bluff</v-btn>
    </v-form>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'bluff',
  props: {
    fobbit: undefined,
  },
  data() {
    return {
      errors: [],
      submittedBluff: undefined,
      form: {
        bluff: '',
      },
    };
  },
  computed: {
    ...mapState({
    }),
  },
  methods: {
    bluff() {
      this.$store.dispatch(
        'bluff',
        { fobbit: this.fobbit.id, text: this.form.bluff },
      )
        .then(() => {
          this.fobbit.have_bluffed = true;
        });
    },
  },
};
</script>
