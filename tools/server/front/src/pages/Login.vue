<!--
todo: finish implementing the form validation feature
-->

<template>
	<div class="login">
		<div class="form-container">
		<p v-on:click="submitForm">Login page</p>

		<form v-on:submit="submitForm">
			<p :class="{ 'control': true }">
				<input v-model="formData.username" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('username') }" name="username" type="text" placeholder="Username" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.pass" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('pass') }" name="pass" type="password" placeholder="Password" required>
			</p>
			
			<input type="submit" name="submit" class="submit">
			<div class="form-error" v-if="loginError">Check the username or password.</div>
		</form>
		</div>
	</div>
</template>

<script> 
import auth from "../auth";



export default {
	data() {
		return {
			formData: {
				username: "",
				pass: ""
			},
			loginError: false
		}
	},

	methods : {
		submitForm(e) {
			e.preventDefault();
			this.$http.post('http://127.0.0.1:5000/login', {
					"username" : this.formData.username,
					"password" : this.formData.pass
				})
				.then(
					(response) => {
						if(response.data.response == "ok"){
							auth.set_auth(response.data.token, this.formData.username)
							this.loginError = false;
							window.location.href = "/";
						}
						else{
							this.loginError = true;
						}
					}, 
					(response) => {
						console.log("POST FAILED.");
						this.loginError = true;
					}
				);
		}
	}
}
</script>