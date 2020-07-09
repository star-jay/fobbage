<template>
  <v-container fluid fill-height>
    <v-layout justify-center>
      <v-flex xs12 sm8 md4>

        <v-card class="elevation-12">
          <v-toolbar dark color="primary" dense flat>
            <v-toolbar-title>Registration</v-toolbar-title>
          </v-toolbar>
          <div v-if="!submitted">
            <v-card-text v-if="errors.non_field_errors">
              <v-alert :key=error v-for="error in errors.non_field_errors"
                :title="error"
                :closable="false"
                type="error"
                center
                show-icon
                >
              </v-alert>
            </v-card-text>
            <v-card-text>
              <v-form
                @submit.prevent="register"
                id="register"
                ref="registration"
                lazy-validation
              >
                <v-text-field
                  v-model="form.username"
                  prepend-icon="person"
                  name="username"
                  label="Username"
                  :rules="rules.username"
                  type="text"></v-text-field>
                <v-text-field
                  v-model="form.first_name"
                  prepend-icon="person"
                  name="first_name"
                  label="First Name"
                  :rules="rules.first_name"
                  type="text"></v-text-field>
                <v-text-field
                  v-model="form.last_name"
                  prepend-icon="person"
                  name="last_name"
                  label="Last Name"
                  :rules="rules.last_name"
                  type="text"></v-text-field>
                <v-text-field
                  v-model="form.email"
                  prepend-icon="email"
                  name="email"
                  label="Email"
                  :error-messages="errors.email"
                  :rules="rules.email"
                  type="email"></v-text-field>
                <v-text-field
                  v-model="form.password"
                  prepend-icon="lock"
                  name="password"
                  label="Password"
                  id="password"
                  :rules="rules.password"
                  :error-messages="errors.password"
                  type="password"></v-text-field>
                <v-text-field
                  v-model="form.password2"
                  prepend-icon="loop"
                  name="password2"
                  label="Repeat your password"
                  id="password2"
                  :rules="rules.password2"
                  type="password"></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn type="submit" color="primary" form="register">Register</v-btn>
            </v-card-actions>
          </div>
          <v-card-text v-else>
            <p>Thank you.</p>
            <p>
              Your account has been created.
              Please wait while we redirect you to the  <router-link :to="{name: 'login'}">login</router-link> page.
            </p>
          </v-card-text>
        </v-card>
        <p class="ma-2">
          Already have an account? Login <router-link :to="{name: 'login'}">here</router-link>.
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { setTimeout } from 'timers';

export default {
  name: 'register',
  data() {
    return {
      errors: {},
      submitted: false,
      form: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        password2: '',
      },
      rules: {
        username: [
          v => !!v || 'Username is required',
          v => (v && v.length <= 150) || 'Username must be less than 150 characters',
        ],
        email: [
          v => !!v || 'Email is required',
        ],
        first_name: [
          v => !!v || 'First Name is required',
          v => (v && v.length <= 30) || 'First Name must be less than 30 characters',
        ],
        last_name: [
          v => !!v || 'Last Name is required',
          v => (v && v.length <= 30) || 'Last Name must be less than 150 characters',
        ],
        password: [
          v => !!v || 'Password is required',
          v => (v && v.length > 7) || 'Your password should be at least 8 characters',
          v => (this.form.password2.length === 0) || (v && v === this.form.password2) || 'The passwords did not match',
        ],
        password2: [
          v => !!v || 'Please re-enter the password',
          v => (v && v === this.form.password) || 'The passwords did not match',
        ],
      },
    };
  },
  computed: {
    ...mapGetters({
      loading: 'authLoading',
    }),
  },
  methods: {
    register() {
      this.errors = {}; // clear errors that were returned by the action
      if (this.$refs.registration.validate()) {
        // Fill in the hostname where this app is running.
        this.form.hostname = window.location.host;
        this.$store.dispatch('register', this.form)
          .then(() => {
            this.submitted = true;
            setTimeout(()=>{
              router.push({ name: 'login' });
            }, 3000)
          })
          .catch((error) => {
            this.errors = error.response.data;
          });
      }
    },
  },
};
</script>
