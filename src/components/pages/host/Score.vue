<template>
  <div class="ma-4" v-if="score">
    <!-- CORRECT -->
    <div v-if="score.is_correct">
      <p>The correct answer was:</p>
      <b>{{ score.text }}</b>
      <p class="my-2">Players who guessed correctly: </p>
      <span v-for="guess in score.guesses" :key="guess.player.id">
        {{ guess.player.username }}: + {{ guess.score }}
        </span>
    </div>
    <!-- BLUFF -->
    <div v-else>
      <p class="title">{{ score.text }}</p>
      <div>
        <p>
          Was a bluff from:
          <span v-for="score in score.scores" :key="score.player.id">
            <b>{{ score.player.username }}</b>
          </span>
        </p>
          And it was worth: <b>{{ score.scores[0].score }}</b> points!
      </div>
      <!-- guesses -->
      <p class="my-2 caption" v-if="score.guesses.length">
        Players who guessed this was the correct answer:
      </p>
      <!-- Likes -->
      <p class="my-2" v-if="score.like_answers.length">
        Players who liked this answer:
      </p>
        <span v-for="like in score.like_answers" :key="like.id">
          <b>{{ like.player.username }}</b>
        </span>
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
