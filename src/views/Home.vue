<template>
  <div>
    <NavigationBar/>
    <v-container>
        <router-view/>
    </v-container>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue';

export default {
  name: 'Play',
  components: {
    NavigationBar,
  },
};
</script>
