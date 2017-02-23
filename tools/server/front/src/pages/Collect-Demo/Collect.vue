<template>
	<div id="collect-container">
		<component :is="currentView"></component>
	</div>
</template>
<script>

var initSessionStorage = () => {

	// sessionStorage.setItem('email', "");
	// sessionStorage.setItem('name', "");
	// sessionStorage.setItem('lastname', "");
	// sessionStorage.setItem('age', "");
	// sessionStorage.setItem('gender', "");

	// sessionStorage.setItem('dataChunk1', "");
	// sessionStorage.setItem('mouseDataChunk1', "");

}

initSessionStorage();


import PersonalData from "./PersonalData.vue"
import KeyTest1 	from "./KeyTest1.vue"
import MouseTest1 	from "./MouseTest1.vue"
import Final 		from "./Final.vue"
import Stats 		from "./Stats.vue"

export default {
	data(){
		return {
			currentView: 'PersonalData'
		}
	},

	components: {
		'PersonalData': PersonalData,
		'KeyTest1': KeyTest1,
		'MouseTest1': MouseTest1,
		'Final': Final,
		'Stats': Stats
	}
}


</script>