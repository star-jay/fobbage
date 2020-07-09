<template>
  <v-app-bar
    dark
    app
    class="primary"
  >
    <v-toolbar-title >Fobbage</v-toolbar-title>
    <v-spacer></v-spacer>

     <v-menu
      transition="slide-y-transition"
      bottom
      offset-y
    >
      <template v-slot:activator="{ on }">
        <v-btn
          dark
          icon
          v-on="on"
        >
          <v-icon>person</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          @click="logout"
        >
        <v-list-item-title>Logout/Login</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

  </v-app-bar>
</template>

<script>

import { mapGetters } from 'vuex';

export default {
  name: 'NavigationBar',
  data() {
    return {
      menu: {
        title: 'Menu',
        items: [
          {
            link: 'home',
            icon: 'linear_scale',
            title: 'Home',
          },
          {
            link: 'play',
            icon: 'gesture',
            title: 'Play',
          },
          {
            link: 'register',
            icon: 'gesture',
            title: 'Register',
          },
        ],
      },
    };
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push({ name: 'login' });
        });
    },
  },
  props: {
    title: String,
  },
};
</script>
