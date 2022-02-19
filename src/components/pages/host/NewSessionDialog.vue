<template>
  <v-dialog
    v-model="dialog"
    width="500"
  >
    <template v-slot:activator="{ on }">
      <v-btn text v-on="on" >
      <!-- <v-icon class="pr-2">add</v-icon> -->
        {{ quiz.title }}
      </v-btn>
    </template>

    <v-card>
      <v-card-title
        class="headline"
        primary-title
      >
        New Session
      </v-card-title>

      <v-form ref="createNewSessionForm"
        v-model="valid" @submit.prevent="createNewSession"
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
            v-model="form.name"
            label="Name*"
            name="name"
            required
            :rules="nameRules"
            :error-messages="errors.name"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Close</v-btn>
          <v-btn color="primary" type="submit" text>Host</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    quiz: undefined,
  },
  data() {
    return {
      dialog: false,
      form: {
        name: this.quiz.title,
      },
      nameRules: [
        v => !!v || 'Name is required',
      ],
      valid: false,
      errors: {},
    };
  },
  methods: {
    createNewSession() {
      if (this.$refs.createNewSessionForm.validate()) {
        this.$store.dispatch('createSession', { ...this.form, quiz: this.quiz.id })
          .then((session) => {
            this.$router.push({
              name: 'session-detail',
              params: { sessionId: session.id },
            });
            this.$refs.createNewSessionForm.reset();
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
