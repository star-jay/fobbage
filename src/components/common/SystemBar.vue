<template>
  <v-system-bar
    dark
    app
    class="primary"
    dense
  >
    <!-- <v-toolbar-title>Fobbage</v-toolbar-title> -->
    <v-spacer></v-spacer>
      {{ $store.state.auth.userInfo.username }}
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
          <v-icon>account</v-icon>
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
  </v-system-bar>
</template>

<script>

import { } from 'vuex';

export default {
  name: 'SystemBar',
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
