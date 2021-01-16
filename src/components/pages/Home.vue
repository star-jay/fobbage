<template>
  <v-container>
      Home
    <v-row class="ma-2">
      <v-card
        class="mx-auto"
        max-width="344"
        href="play"
      >
        <v-card-title class="display-1">
          Play
        </v-card-title>

        <v-card-text>
          <div class="text--primary">
            Join a session and battle your friends in a game of wits!
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
          <v-card
        class="mx-auto"
        max-width="344"
      >
        <v-card-text>
          <div>Word of the Day</div>
          <p class="display-1 text--primary">
            be•nev•o•lent
          </p>
          <p>adjective</p>
          <div class="text--primary">
            well meaning and kindly.<br>
            "a benevolent smile"
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            color="deep-purple accent-4"
          >
            Learn More
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'Home',
  components: {
  },
};
</script>
