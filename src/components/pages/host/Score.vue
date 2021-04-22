<template>
  <div v-if="score">
    <h3>{{ score.text }}</h3>
      <div v-if="score.is_correct">
        <h4>Was the correct answer!</h4>
      </div>
      <div v-else>
        <h4>Was a bluff from:</h4>
        <span v-for="score in score.scores" :key="score.player.id">
          {{ score.player.username }}: + {{ score.score }}
        </span>
      </div>
      <br/>
      <div>

      <h3>Players who guessed this answer:</h3>
        <span v-for="guess in score.guesses" :key="guess.id">
          {{ guess.player.username }}
          <span v-if="score.is_correct"> +{{ guess.score }} </span>
        </span>
      <br/>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Score',

  props: {
    score: null,
  },
};
</script>
