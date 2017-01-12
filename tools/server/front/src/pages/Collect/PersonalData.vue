<template>
	<div>
		<h2 style="text-align:center">Personal Data Collecting</h2>
		<div class="form-container">
		<p>Enter your personal data: </p>

		<form @submit.prevent="validateBeforeSubmit">
			<p class="control">
			<input name="email" v-model="email" v-validate.initial="email" data-vv-rules="required|email" :class="{'input': true, 'is-danger': errors.has('email') }" type="text" placeholder="Email">
			</p>
			<p class="control">
			<input name="name" v-model="name" v-validate.initial="name" data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('name') }" type="text" placeholder="Name">
			</p>
			<p class="control">
			<input name="lastname" v-model="lastname" v-validate.initial="lastname" data-vv-rules="required" :class="{'input': true, 'is-danger': errors.has('lastname') }" type="text" placeholder="Lastname">
			</p>
			<p class="control">
			<input name="age" v-model="age" v-validate.initial="age" data-vv-rules="required|numeric" :class="{'input': true, 'is-danger': errors.has('age') }" type="text" placeholder="Age">
			</p>
			<p class="control">
				<label class="radio">
					<input v-model="gender" class="radio" name="gender" v-validate data-vv-rules="required|in:male, female" value="male" type="radio">
					Male
				</label>
				<label class="radio">
					<input v-model="gender" class="radio" name="gender" value="female" type="radio">
					Female
				</label><br>
			<span class="help checkbox-danger" v-show="errors.has('gender')">{{ errors.first('gender') }}</span><br>
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
			email: "",
			name: "",
			lastname: "",
			age: "",
			gender: ""
		}
	},

	methods : {
		validateBeforeSubmit() { 

			this.$validator.validateAll().then(success => {
				if (! success) {
					console.log("Validate");
					return;
				}
				
				sessionStorage.setItem('email', this.email);
				sessionStorage.setItem('name', this.name);
				sessionStorage.setItem('lastname', this.lastname);
				sessionStorage.setItem('age', this.age);
				sessionStorage.setItem('gender', this.gender);

				this.$parent._data.currentView = "KeyTest1";

			});
		}
	}
}
</script>