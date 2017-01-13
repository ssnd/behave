<template>
	<div id="collect-container">
		<component :is="currentView"></component>
	</div>
</template>
<script>

var initSessionStorage = () => {

	sessionStorage.setItem('email', "");
	sessionStorage.setItem('name', "");
	sessionStorage.setItem('lastname', "");
	sessionStorage.setItem('age', "");
	sessionStorage.setItem('gender', "");

	sessionStorage.setItem('dataChunk1', "");
	sessionStorage.setItem('dataChunk2', "");
	sessionStorage.setItem('dataChunk3', "");
	sessionStorage.setItem('dataChunk4', "");
	sessionStorage.setItem('mouseDataChunk1', "");
	sessionStorage.setItem('mouseDataChunk2', "");
	sessionStorage.setItem('mouseDataChunk3', "");
	sessionStorage.setItem('mouseDataChunk4', "");

}

initSessionStorage();


import PersonalData from "./PersonalData.vue"
import KeyTest1 	from "./KeyTest1.vue"
import KeyTest2 	from "./KeyTest2.vue"
import KeyTest3 	from "./KeyTest3.vue"
import KeyTest4 	from "./KeyTest4.vue"
import MouseTest1 	from "./MouseTest1.vue"
import MouseTest2 	from "./MouseTest2.vue"
import MouseTest3 	from "./MouseTest3.vue"
import MouseTest4 	from "./MouseTest4.vue"
import Final 		from "./Final.vue"

export default {
	data(){
		return {
			currentView: 'PersonalData'
		}
	},

	components: {
		'PersonalData': PersonalData,
		'KeyTest1': KeyTest1,
		'KeyTest2': KeyTest2,
		'KeyTest3': KeyTest3,
		'KeyTest4': KeyTest4,
		'MouseTest1': MouseTest1,
		'MouseTest2': MouseTest2,
		'MouseTest3': MouseTest3,
		'MouseTest4': MouseTest4,
		'Final': Final
	}
}


</script>