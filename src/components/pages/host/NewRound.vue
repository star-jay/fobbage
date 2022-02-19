<template>
  <v-dialog
    v-model="dialog"
    width="500"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="mx-auto my-2"
        v-on="on"
      >
        New Round
      </v-btn>
    </template>

    <v-card>
      <v-card-title
        class="headline"
        primary-title
      >
        New Round
      </v-card-title>

      <v-form ref="createNewRoundForm"
        v-model="valid"
        @submit.prevent="createNewRound"
        lazy-validation
      >
        <v-card-text>
          <v-alert :key='error' v-for="error in errors.non_field_errors"
            :title="error"
            type="error"
            center
            outlined
            >{{ error }}
          </v-alert>
          <v-text-field
            v-model.number="form.multiplier"
            label="Multiplier"
            name="multiplier"
            required
            type="number"
          ></v-text-field>
          <v-text-field
            v-model.number="form.numberOfQuestions"
            label="Questions Per Round"
            name="numberOfQuestions"
            required
            type="number"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" type="submit" text>Start</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'NewRound',
  props: ['session'],
  data() {
    return {
      dialog: false,
      form: {
        numberOfQuestions: 3,
        multiplier: 1,
      },
      valid: false,
      errors: {},
    };
  },
  methods: {
    createNewRound() {
      if (this.$refs.createNewRoundForm.validate()) {
        this.$store.dispatch('newRound', { ...this.form, sessionId: this.session.id })
          .then(() => {
            this.dialog = false;
          })
          .catch((error) => {
            if (error.response) {
              this.errors = error.response.data;
            } else {
              console.log(error.message);
            }
          });
      }
    },
  },
};
</script>
