<template>
  <v-list flat>
    <v-list-item-group v-model="sessionlist" color="primary">
      <v-list-item
        v-for="session in sessionlist"
        :key="session.id"
        @click="$router.push({
          name: 'fobbit-detail',
          params: { sessionId: session.id },
        })"
      >
        <v-list-item-content>
          <v-list-item-title v-text="session.name">
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
      sessionlist: state => state.quizes.sessions,
    }),
  },
  methods: {

  },
  created() {
    this.$store.dispatch('listSessions');
  },
};
</script>
