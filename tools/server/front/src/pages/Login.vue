<!--
todo: finish implementing the form validation feature
-->

<template>
	<div class="login">

		<p v-on:click="submitForm">Login page</p>

		<form v-on:submit="submitForm">
			<p :class="{ 'control': true }">
				<input v-model="formData.email" v-validate data-vv-rules="required|email" :class="{'input': true, 'is-danger': errors.has('email') }" name="email" type="text" placeholder="Email">
				<span v-show="errors.has('email')" class="help is-danger">{{ errors.first('email') }}</span>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.pass" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('pass') }" name="pass" type="password" placeholder="Password">
				<span v-show="errors.has('pass')" class="help is-danger">{{ errors.first('pass') }}</span>
			</p>

			<input type="submit" name="submit">
		</form>

	</div>
</template>

<script> 

export default {
	data() {
		return {
			formData: {
				email: "",
				pass: ""
			}
		}
	},

	methods : {
		submitForm(e) {
			e.preventDefault();
			this.$http.post('http://127.0.0.1:5000/login', {
					"username" : this.formData.email,
					"password" : this.formData.pass
				})
				.then(
					(response) => {
						console.log(response);
					}, 
					(response) => {
						console.log("POST FAILED.");
					}
				);
		}
	}
}
</script>