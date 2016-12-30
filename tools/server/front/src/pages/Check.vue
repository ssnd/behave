<template>
	<div id="bh">
		<div id="bh-pattern">
		<span>Type in this text: </span><br>
		After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice! when she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: she could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried.</div>
		<textarea name="input" id="bh-input" rows="10" v-on:keydown="setKeyDuration" v-on:keyup="keypressHandle($event)"></textarea><br>
		<button v-on:click="pushBehaveData" id="bh-submit">
			Submit
		</button> <span class="key-len">{{ keyHandler.length }}</span>
	</div>
</template>
<script>
	var keyDurationHandler = 0;
	var userName = "58336ace29d23e4cea259a27";
	export default {
		data: function(){
			return {
			keyHandler: []
			}
		},
		methods: {
			pushBehaveData: function(){
				var serverCheckResponse = 0;
				console.log(this.keyHandler);
				// post 
				this.$http.post('http://127.0.0.1:5000/check', {
				"data" : this.keyHandler
				}).then((response) => {
					serverCheckResponse = parseFloat((response.body).substring(1));
					console.log(serverCheckResponse);
					if(serverCheckResponse > 0.5){
						window.location.href = "granted.html";
					}
					else{
						window.location.href = "denied.html";
					}
				}, (response) => {console.log("POST FAILED.")});
			},
			keypressHandle: function(event){
				if(this.keyHandler.length < 90){
					this.keyHandler.push({
						keycode: event.keyCode, 
						timestamp: +new Date(),
						key_duration: new Date() - keyDurationHandler
					});
				}
			},
			setKeyDuration: function(){
				keyDurationHandler = new Date();
			}
		}
	}
</script>