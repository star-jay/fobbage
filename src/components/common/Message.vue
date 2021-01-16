<template>
  <div class="card">

    <div class="card-content">

      <div class="media-content">
        <p class="title is-4">{{ message.user }}</p>
      </div>

      <div class="content">
        {{ message.message }}
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Bluff',
  props: ['message'],
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
