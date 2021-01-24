<template>
  <div>
    <div v-if="active_fobbit.have_bluffed">
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
  data() {
    return {
      errors: [],
      form: {
        bluff: '',
      },
    };
  },
  computed: {
    ...mapState({
      active_fobbit: (state) => state.quizes.active_fobbit,
    }),
  },
  methods: {
    bluff() {
      this.$store.dispatch('bluff', { text: this.form.bluff });
    },
  },
};
</script>
