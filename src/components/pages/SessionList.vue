<template>
  <v-list flat>
    <v-subheader>Quizes</v-subheader>
    <v-list-item-group v-model="sessionlist" color="primary">
      <v-list-item
        v-for="session in sessionlist"
        :key="session.name"
        :to="'/'+session.id"
      >
        <v-list-item-content>
          <v-list-item-title v-text="session.title">
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'SessionList',
  computed: {
    ...mapState({
      sessionlist: (state) => state.quizes.sessions,
    }),
  },
  methods: {
    joinQuiz(id) {
      this.$store.dispatch('joinSession', { id });
    },
  },
  created() {
    this.$store.dispatch('getSessionList');
  },
};
</script>
