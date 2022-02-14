<template>
  <div>
    <SystemBar/>
     <v-main>
      <router-view/>
     </v-main>
  </div>
</template>

<script>
import SystemBar from '@/components/common/SystemBar.vue';

export default {
  name: 'BaseLayout',
  components: {
    SystemBar,
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
  computed: {
    session() {
      return this.$store.getters.session(this.sessionId);
    },
    calculatedIndex() {
      if (this.session && this.session.fobbits) {
        return this.session.fobbits.findIndex(id => id === this.session.active_fobbit.id) + 1;
      }
      return 1;
    },
  },
};
</script>
