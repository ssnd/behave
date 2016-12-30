<template>
	<div>
		<div id="home-selectors">
        <v-link href="/register">Register</v-link>
        <v-link href="/training">Training</v-link>
        <v-link href="/check">Check</v-link></div>
    </div>
</template>

<script>
  import VLink from '../components/VLink.vue'

  export default {
    components: {
      VLink
    }
  }
</script>