<template>
  <v-navigation-drawer
    dark
    app
    permanent
    right
  >
    <div v-if="fobbit.status == 0" class="ma-2">
      <h4>
        Waiting on:
      </h4>
      <v-list flat>
        <v-list-item
          v-for="player in fobbit.players_without_bluff"
          :key="player.id"
        >
          <v-list-item-content>
            {{ player.username }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>
    <div v-if="fobbit.status == 1">
      <v-list flat>
        <v-list-item
          v-for="player in fobbit.players_without_guess"
          :key="player.id"
        >
          <v-list-item-content>
            {{ player.username }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>

    <v-container ma-2>
      <v-row ma-2>
        <v-btn
          @click="$store.dispatch('nextQuestion', ({ sessionId: fobbit.session }))"
          class="mx-auto my-1"
        >
          Next question
        </v-btn>
      </v-row>
      <v-row>
        <v-btn
          @click="$store.dispatch('resetFobbit', { fobbit })"
          class="mx-auto my-1"
        >
          Reset
        </v-btn>
      </v-row>
      <v-row>
        <v-btn
          @click="$store.dispatch('generateAnswersForFobbit', { fobbit })"
          class="mx-auto my-1"
        >
          Generate Answers
        </v-btn>
      </v-row>
      <v-row>
        <v-btn
          @click="$store.dispatch('finishFobbit', { fobbit })"
          class="mx-auto my-1"
        >
          Finish
        </v-btn>
      </v-row>
      <v-row>
        <v-btn
          :to="{ name: 'scores' }"
          class="mx-auto my-1"
        >
          Scores
        </v-btn>
      </v-row>
    </v-container>

  </v-navigation-drawer>
</template>

<script>

import { } from 'vuex';

export default {
  name: 'PlayerList',
  props: ['fobbit'],
  methods: {},
  data() {
    return {
      fobbitIndex: 1,
    };
  },
};
</script>
