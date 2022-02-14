<template>
  <v-app dark class="ma-2">
    <router-view/>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  components: {
  },
  created() {
    document.title = 'Fobbage';
  },
};
</script>
