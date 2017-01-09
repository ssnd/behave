
<template>
<div>
	<h2 style="text-align:center">Keyboard Typing Test 1</h2>
	<div id="bh">
		<div id="bh-pattern">
		<span>Type in this text: </span><br>
		After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice! </div>
		<textarea name="input" id="bh-input" rows="10" v-on:keydown="setKeyDuration" v-on:keyup="keypressHandle($event)"></textarea><br>
		<input type="submit" name="submit" class="submit" value="Next" v-on:click="pushBehaveData"> 
		<span class="key-len">{{ keyHandler.length }}</span>
		<div class="form-error" v-if="warning">You should type at least 40 characters.</div>
	</div>
</div>
</template>
<script>

	var keyDurationHandler = 0;

	export default {

		data (){
			return {
				keyHandler: [],
				warning: false
			}
		},

		methods: {

			pushBehaveData () {
				if(this.keyHandler.length >= 40){
			sessionStorage.setItem('dataChunk1', this.keyHandler);
			this.warning = false;
			this.$parent._data.currentView = "KeyTest2";
		}
		else{
			this.warning = true;
		}
			},


			keypressHandle(event){

				if(this.keyHandler.length < 40){
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