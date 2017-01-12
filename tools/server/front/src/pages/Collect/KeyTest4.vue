<template>
<div>
	<h2 style="text-align:center">Keyboard Typing Test 4</h2>
	<div id="bh">
		<div id="bh-pattern">
		<span>Retype this text: </span><br>
		When Mr. and Mrs. Dursley woke up on the dull, gray Tuesday our story
starts, there was nothing about the cloudy sky outside to suggest that
strange and mysterious things would soon be happening all over the
country. Mr. Dursley hummed as he picked out his most boring tie for
work, and Mrs. Dursley gossiped away happily as she wrestled a screaming
Dudley into his high chair.</div>
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
					sessionStorage.setItem('dataChunk4', jsonString);
					this.warning = false;
					this.$parent._data.currentView = "MouseTest";
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