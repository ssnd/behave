
<template>
<div>
  <h2 style="text-align:center">Keyboard Typing Test 2</h2>
  <div id="bh">
    <div id="bh-pattern">
    <span>Type in this text: </span><br>
    When she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: she could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried.</div>
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
			sessionStorage.setItem('dataChunk2', this.keyHandler);
			this.warning = false;
			this.$parent._data.currentView = "MouseTest";
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