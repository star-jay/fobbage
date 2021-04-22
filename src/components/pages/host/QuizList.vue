<template>
  <v-list flat>
    <v-list-item-group v-model="quizList" color="primary">
      <v-list-item
        v-for="quiz in quizList"
        :key="quiz.id"
      >
        <v-list-item-content>
          <NewSessionDialog :quiz='quiz'/>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>

  </v-list>
</template>

<script>
import { mapState } from 'vuex';
import NewSessionDialog from './NewSessionDialog.vue';

export default {
  name: 'QuizList',
  components: {
    NewSessionDialog,
  },
  data() {
    return {
      quiz: undefined,
      sessionDialog: false,
    };
  },
  computed: {
    ...mapState({
      quizList: (state) => state.quizes.quizes,
    }),
  },
  methods: {
  },
  created() {
    this.$store.dispatch('listQuizes');
  },
};
</script>
