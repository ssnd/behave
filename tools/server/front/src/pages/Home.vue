<template>
	<div>
		<div id="home-selectors">
        <v-link href="/register">Register</v-link>
        <v-link href="/training">Training</v-link>
        <v-link href="/check">Check</v-link>
        <button v-if="logged_in" class="logout" v-on:click="logout()">Logout ({{ logged_user }})</button>
        <button v-if="!logged_in" class="logout" v-on:click="login()">Login</button>
      </div>
  </div>
</template>

<script>
  import VLink from '../components/VLink.vue'
  import auth from "../auth";

  export default {
    components: {
      VLink
    },
    data() {
      return {
        logged_in: (localStorage.getItem("logged_in") == 1),
        logged_user: localStorage.getItem("logged_user")      
      }
    },
    methods: {
      logout(){
        this.$http.post('http://127.0.0.1:5000/logout').then(
          (response) => {
            if(response.data.status == "ok"){
              auth.set_logout();
              this.logged_in = false;
            }
          }, 
          (response) => {
            console.log("POST FAILED.");
          }
        );
      },
      login(){
        window.location.href = "/login"
      }
    }
  }
</script>