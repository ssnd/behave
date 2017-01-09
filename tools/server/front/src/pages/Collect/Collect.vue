<template>
	<div id="collect-container">
		<component :is="currentView"></component>
	</div>
</template>
<script>

var initSessionStorage = () => {

	sessionStorage.setItem('personalData', "");
	sessionStorage.setItem('dataChunk1', "");
	sessionStorage.setItem('dataChunk2', "");
	sessionStorage.setItem('mouseDataChunk', "");

}

initSessionStorage();


import PersonalData from "./PersonalData.vue"
import KeyTest1 from "./KeyTest1.vue"
import KeyTest2 from "./KeyTest2.vue"
import MouseTest from "./MouseTest.vue"

export default {
	data(){
		return {
			currentView: 'MouseTest',
			submitData: {
				personalData: "",
				dataChunk1: "",
				dataChunk2: "",
				mouseDataChunk: ""
			}
		}
	},

	components: {
		'PersonalData': PersonalData,
		'KeyTest1': KeyTest1,
		'KeyTest2': KeyTest2,
		'MouseTest': MouseTest,

	}
}


</script>