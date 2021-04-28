<template>
  <div>
    <h2>
      {{ fobbit.question.text }}
    </h2>

    <div v-if="fobbit.status == 0">
      <v-img v-if="fobbit.question.image_url" :src="fobbit.question.image_url" />
      <h3>
        People who need to bluff:
      </h3>
      {{ fobbit.players_without_bluff.map(player => player.username) }}
    </div>
    <div v-if="fobbit.status == 1">
      <div>
        <v-list flat>
          <v-list-item
            v-for="answer in fobbit.answers"
            :key="answer.id"
          >
            <v-list-item-content>
              {{ answer.order }}. {{ answer.text.toLowerCase()}}
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
      <h3>
        People who need to guess:
      </h3>
      {{ fobbit.players_without_guess.map(player => player.username) }}
    </div>
    <div v-if="fobbit.status == 2">
      <router-view :fobbit="fobbit"/>
      <v-btn @click="$store.dispatch('nextQuestion', ({ sessionId: fobbit.session }))">
        Next question
      </v-btn>
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
    <v-btn :to="{ name: 'scores' }">
      Scores
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
