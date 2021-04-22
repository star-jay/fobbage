<template>
  <div>
    <v-row class="ma-2">
      <v-card
        class="mx-auto"
        max-width="344"
      >
        <v-card-title>
          Continue with session:
        </v-card-title>
        <SessionList />
      </v-card>
      <v-card
        class="mx-auto"
        max-width="344"
      >
        <v-card-title>
          Start a new session
        </v-card-title>
        <QuizList />
      </v-card>
    </v-row>
  </div>
</template>

<script>
import SessionList from './SessionList.vue';
import QuizList from './QuizList.vue';

export default {
  name: 'Host',
  components: { SessionList, QuizList },
  methods: {},
};
</script>
