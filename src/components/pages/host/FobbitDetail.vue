<template>
  <div>
    <h2>
    {{ fobbit.question.text }}
    </h2>
    <div v-if="fobbit.status == 0">
      <h3>
        People who need to bluff:
      </h3>
      {{ fobbit.players_without_bluff }}
    </div>
    <div v-if="fobbit.status == 1">
      <h3>
        People who need to guess:
      </h3>
      {{ fobbit.players_without_guess }}
    </div>
     <v-btn @click="$store.dispatch('resetFobbit', { fobbit })">
      Reset
    </v-btn>
     <v-btn @click="$store.dispatch('generateAnswersForFobbit', { fobbit })">
      Generate Answers
    </v-btn>
    <v-btn @click="$store.dispatch('finishFobbit', { fobbit })">
      Finish
    </v-btn>
  </div>
</template>

<script>

export default {
  name: 'FobbitDetail',
  props: {
    fobbit: undefined,
  },
  created() {
  },
  computed: {

  },
  methods: {
    refresh() {
    },

  },
};
</script>
