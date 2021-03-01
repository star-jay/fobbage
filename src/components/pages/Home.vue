<template>
  <v-container>
      Home
    <v-row class="ma-2">
      <v-card
        class="mx-auto"
        max-width="344"
        :to="{name: 'play'}"
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
        :to="{name: 'host'}"
      >
        <v-card-title class="display-1">
          Host
        </v-card-title>

        <v-card-text>
          <div class="text--primary">
            Host an existing quiz for your friends!
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            color="accent-4"
          >
            Host
          </v-btn>
        </v-card-actions>
      </v-card>

      <v-card
        class="mx-auto"
        max-width="344"
        href="create"
      >
        <v-card-title class="display-1">
          Create a new quiz
        </v-card-title>

        <v-card-text>
          <div class="text--primary">
            Create a brand new quiz using existing questions or your own.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            color="accent-4"
          >
            Create
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
