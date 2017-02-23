<template>
	<div id="db-container">
		<h1 align="center">Database explorer</h1>

		<component :is="currentView"></component>

	</div>
</template>

<script>
import List from "./List.vue"

export default {
	data(){
		return {
			currentView: 'List'
		}
	},

	components: {
		'List' : List,
	}
}

</script>