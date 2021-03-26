<template>
  <div>
    Scoreboard
      <v-btn @click="$store.dispatch('nextQuestion', ({ sessionId }))">
        Next question
      </v-btn>
  </div>

</template>

<script>

export default {
  name: 'Scoreboard',
  components: {
  },
  props: {
    fobbit: undefined,
    session: undefined,
  },
  data() {
    return {
    };
  },
  methods: {
    resetIndex() {
    },
  },
  watch: {
    // fobbit: 'resetIndex',
  },

};
</script>
