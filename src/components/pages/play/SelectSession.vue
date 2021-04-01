<template>
  <v-list flat>
    <v-subheader>Select a session to join it!</v-subheader>

    <v-card
        class="mx-auto"
        max-width="344"
        v-for="session in sessionlist"
        :key="session.id"
        :to="''+session.id"
      >
        <v-card-title class="display-1">
          {{ session.name }}
        </v-card-title>
        <v-card-text>
          <div class="text--primary">
            {{ session.owner.username }}
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            color="accent-4"
          >
            Play now
          </v-btn>
        </v-card-actions>
      </v-card>

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
    joinSession(id) {
      this.$store.dispatch('joinSession', { id });
    },
  },
  created() {
    this.$store.dispatch('listSessions');
  },
};
</script>
