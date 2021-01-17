<template>
  <div>
    <NavigationBar/>
     <v-main>
      <router-view/>
     </v-main>
  </div>
</template>

<script>
import NavigationBar from '@/components/common/NavigationBar.vue';

export default {
  name: 'BaseLayout',
  components: {
    NavigationBar,
  },
  created() {
    this.connect();
    this.$store.dispatch('retrieveUserInfo');
  },
  methods: {
    connect() {
      if (!this.$store.getters.isAuthenticated) {
        //
      } else {
        this.$store.dispatch('retrieveUserInfo');
      }
    },
  },
};
</script>
