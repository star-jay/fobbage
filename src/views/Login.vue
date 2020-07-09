<template>
<v-container fluid fill-height>
    <v-layout justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="primary" dense flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="login" id="login">
              <v-text-field
                v-model="form.username"
                prepend-icon="person"
                name="username"
                label="username"
                autocomplete="username"
                type="username"></v-text-field>
              <v-text-field
                v-model="form.password"
                prepend-icon="lock"
                name="password"
                label="Password"
                id="password"
                autocomplete="current-password"
                type="password"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn type="submit" color="primary" form="login">Login</v-btn>
          </v-card-actions>
        </v-card>
        <p class="ma-2 pa-2 text-md-center">
          Don't have an account yet? <router-link :to="{name: 'register'}">Create one</router-link>.
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>


<script>
import { mapGetters } from 'vuex';

export default {
  name: 'login',
  data() {
    return {
      errors: [],
      form: {
        username: '',
        password: '',
      },
    };
  },
  computed: {
    ...mapGetters({
      loading: 'authLoading',
    }),
    formIsComplete() {
      return this.form.username && this.form.password;
    },
  },
  methods: {
    login() {
      this.$store.dispatch('login', this.form)
        .then(() => {
          this.$router.push('/');
        })
        .catch((error) => {
          if (error.response) {
            this.errors = error.response.data;
          } else {
            this.errors = { error };
          }
        });
    },
  },
};
</script>
