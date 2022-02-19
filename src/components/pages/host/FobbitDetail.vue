<template>
  <div class="ma-8" >
    <h3>
      {{ fobbit.question.text }}
    </h3>
    <v-img v-if="fobbit.question.image_url" :src="fobbit.question.image_url" />
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
    </div>
      <!-- scoreboard miss -->
    <router-view :fobbit="fobbit"/>
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
