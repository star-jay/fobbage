<template>
  <v-container fluid fill-height>
    <v-layout justify-center>
      <v-flex xs12 sm8 md4>

        <v-card class="elevation-12">
          <v-toolbar dark color="primary" dense flat>
            <v-toolbar-title>Logged out.</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <p>Thank you for playing.</p>
            <p>
              Click <router-link :to="{name: 'login'}">here</router-link> to login again.
            </p>
          </v-card-text>
        </v-card>
       </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { setTimeout } from 'timers';

export default {
  name: 'logout',
  data() {
    return {
      errors: {},
    };
  },
  created(){
    this.logout();
  },
  methods: {
    logout() {
      this.errors = {}; // clear errors that were returned by the action
      this.$store.dispatch('logout')
        .then(() => {
          this.submitted = true;
          setTimeout(3000, ()=>{
            router.push({ name: 'login' });
          })
        })
        .catch((error) => {
          this.errors = error.response.data;
        });
    },
  },
};
</script>
