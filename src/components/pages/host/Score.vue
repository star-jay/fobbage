<template>
  <div v-if="score">
    <h1>{{ score.text }}</h1>
      <div v-if="score.is_correct">
        <h2>Was the correct answer! </h2>
      </div>
      <div v-else>
        <h2 >Was a bluff from: </h2>
        <span v-for="score in score.scores" :key="score.player">
          {{ score.player.username }}: +{{ score.score }}
        </span>
      </div>
      <br/>
      <div>

      <h2 >Players who guessed this answer:</h2>
        <span v-for="guess in score.guesses" :key="guess.id">
          {{ guess.player.username }}
        </span>
      <br/>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Score',

  props: {
    score: undefined,
  },
};
</script>
