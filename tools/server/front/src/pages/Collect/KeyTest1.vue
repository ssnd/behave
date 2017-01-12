<template>
<div>
	<h2 style="text-align:center">Keyboard Typing Test 1</h2>
	<div id="bh">
		<div id="bh-pattern">
		<span>Type in this text: </span><br>
		Mr. Dursley was the director of a firm called Grunnings, which made
drills. He was a big, beefy man with hardly any neck, although he did
have a very large mustache. Mrs. Dursley was thin and blonde and had
nearly twice the usual amount of neck, which came in very useful as she
spent so much of her time craning over garden fences, spying on the
neighbors. The Dursleys had a small son called Dudley and in their
opinion there was no finer boy anywhere.</div>
		<textarea name="input" id="bh-input" rows="10" v-on:keydown="setKeyDuration" v-on:keyup="keypressHandle($event)"></textarea><br>
		<input type="submit" name="submit" class="submit" value="Next" v-on:click="pushBehaveData"> 
		<span class="key-len">{{ keyHandler.length }}</span>
		<div class="form-error" v-if="warning">You should type at least {{ maxChars }} characters.</div>
	</div>
</div>
</template>
<script>

	var keyDurationHandler = 0;

	export default {

		data (){
			return {
				keyHandler: [],
				warning: false,
				maxChars: 130
			}
		},

		methods: {

			pushBehaveData () {
				if(this.keyHandler.length >= this.maxChars){
					let jsonString = JSON.stringify(this.keyHandler);
					sessionStorage.setItem('dataChunk1', jsonString);
					this.warning = false;
					this.$parent._data.currentView = "KeyTest2";
			}
			else{
				this.warning = true;
			}
			},


			keypressHandle(event){

				if(this.keyHandler.length < this.maxChars){
					this.keyHandler.push({
						keycode: event.keyCode, 
						timestamp: +new Date(),
						key_duration: new Date() - keyDurationHandler
					});
				}
			},


			setKeyDuration (){
				keyDurationHandler = new Date();
			}
		}
	}
</script>