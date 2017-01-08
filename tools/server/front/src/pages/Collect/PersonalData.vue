<template>
	<div>
		<h2 style="text-align:center">Personal Data Collecting</h2>
		<div class="form-container">
		<p>Enter your personal data: </p>

		<form v-on:submit="submitForm">
			<p :class="{ 'control': true }">
				<input v-model="formData.email" v-validate data-vv-rules="required|email" :class="{'input': true, 'is-danger': errors.has('email') }" name="email" type="text" placeholder="Email" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.name" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('name') }" name="name" type="text" placeholder="First Name" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.lastname" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('lastname') }" name="lastname" type="text" placeholder="Last Name" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.age" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('age') }" name="age" type="text" placeholder="Your Age" required>
			</p>
			<p :class="{ 'control': true }">
				<input v-model="formData.gender" v-validate data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('gender') }" name="gender" type="text" placeholder="Gender" required>
			</p>

			<input type="submit" name="submit" class="submit" value="Next">
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
				name: "",
				lastname: "",
				age: "",
				gender: ""
			}
		}
	},

	methods : {
		submitForm(e) {
			e.preventDefault();
			sessionStorage.setItem('personalData', this.formData);
			this.$parent._data.currentView = "KeyTest1";
		}
	}
}
</script>