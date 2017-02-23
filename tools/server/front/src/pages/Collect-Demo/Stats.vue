<template>
	<div>
		
		<h1 align="center">Keyboard stats</h1>
		<div class="charts">
			<chart-line class="chart-param" title="Press-To-Press time" param="p2p"></chart-line>
			<chart-line class="chart-param" title="Release-To-Release time" param="r2r"></chart-line>
			<chart-line class="chart-param" title="Dwell time" param="dwell"></chart-line>
			<chart-line class="chart-param" title="Flight time" param="flight"></chart-line>
		</div>


		<h1 align="center">Mouse stats</h1>
		<div class="charts">
			<chart-line class="chart-param" title="Mouse speed" param="ms"></chart-line>
			<chart-line class="chart-param" title="Double click speed" param="dbcs"></chart-line>
			<chart-line class="chart-param" title="Left click speed" param="lcs"></chart-line>
			<chart-line class="chart-param" title="Right click speed" param="rcs"></chart-line>

		</div>
	</div>

</template>


<script>

	import ChartLine from "./charts/line.vue"
	
	export default {
		components: {ChartLine},
	}

</script>