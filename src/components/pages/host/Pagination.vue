<template>
  <v-footer dark app height=50 >
    <v-row>
      <v-pagination
        class="ma-auto"
        total-visible="10"
        v-model="fobbitIndex"
        :length="session.fobbits.length"
        @input="setFobbit"
      />
    </v-row>
  </v-footer>
</template>

<script>

import { } from 'vuex';

export default {
  name: 'SystemBar',
  props: ['session'],
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push({ name: 'login' });
        });
    },
    setFobbit(index) {
      this.$store.dispatch(
        'setActiveFobbit',
        { session: this.session, fobbitId: this.session.fobbits[index - 1] },
      );
    },
  },
  data() {
    return {
      fobbitIndex: 1,
    };
  },
};
</script>
