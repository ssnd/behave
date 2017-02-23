<template>
	<div style="text-align:center">
		<h2>
			Thank you for giving information!
		</h2>
		<input type="submit" name="submit" id="mouse-push" class="submit" value="Submit" v-on:click="pushToServer"> 
	</div>
</template>
<script>
	export default{
		methods: {
			pushToServer(e){
				e.preventDefault();
				this.$http.post('http://127.0.0.1:5000/collect', {
					"email":			sessionStorage.getItem('email'),
					"name":				sessionStorage.getItem('name'),
					"lastname":			sessionStorage.getItem('lastname'),
					"age":				sessionStorage.getItem('age'),
					"gender":			sessionStorage.getItem('gender'),
					"dataChunk1":		sessionStorage.getItem('dataChunk1'),
					"dataChunk2":		sessionStorage.getItem('dataChunk2'),
					"dataChunk3":		sessionStorage.getItem('dataChunk3'),
					"dataChunk4":		sessionStorage.getItem('dataChunk4'),
					"mouseDataChunk1":	sessionStorage.getItem('mouseDataChunk1'),
					"mouseDataChunk2":	sessionStorage.getItem('mouseDataChunk2'),
					"mouseDataChunk3":	sessionStorage.getItem('mouseDataChunk3'),
					"mouseDataChunk4":	sessionStorage.getItem('mouseDataChunk4')
				})
				.then(
					(response) => {
						console.log("POST SUCCESS.");
						window.location = "/"
					}, 
					(response) => {
						console.log("POST FAILED.");
					}
				);
			}
		}
	}
</script>