<template>
  <div>
    <NavigationBar/>
     <v-main>
      <router-view/>
     </v-main>
  </div>
</template>

<script>
import NavigationBar from '@/components/common/NavigationBar.vue';

export default {
  name: 'BaseLayout',
  components: {
    NavigationBar,
  },
};
</script>
