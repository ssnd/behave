<!-- 
todo: form validation
-->

<template>
	<div class="register">
		<div class="form-container">
		<p v-on:click="submitForm">Register page</p>

		<form v-on:submit="submitForm">
			<p :class="{ 'control': true }">
				<input v-model="formData.email" v-validate data-vv-rules="required|email" :class="{'input': true, 'is-danger': errors.has('email') }" name="email" type="text" placeholder="Email" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.username" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('username') }" name="username" type="text" placeholder="Username" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.pass" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('pass') }" name="pass" type="password" placeholder="Password" required>
			</p>
			

			<input type="submit" name="submit" class="submit">
		</form>
		</div>
	</div>
</template>

<script> 



export default {
	data() {
		return {
			formData: {
				email: "",
				pass: "",
				username: ""
			}
		}
	},

	methods : {
		submitForm(e) {
			e.preventDefault();
			this.$http.post('http://127.0.0.1:5000/register', {
					"username" : this.formData.username,
					"password" : this.formData.pass,
					"email": this.formData.email
				})
				.then(
					(response) => {
						console.log("POST SUCCESS.");
						window.location.href = "/login";
					}, 
					(response) => {
						console.log("POST FAILED.");
					}
				);
		}
	}
}
</script>