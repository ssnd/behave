<script>

import {Line, mixins} from 'vue-chartjs';
import Behave from "../behave-lib.js"
import math from "mathjs"

export default Line.extend({
	// mixins: [mixins.reactiveProp],
	props : ['chartData', 'param', 'title'],
	mounted() {
		console.log(this)
		this.renderChart(this.chartData)
	},
	methods: {
		updateChart() {

			let values = []
			let strKeyboardData = this.chartData.dataChunk1;

			let keyboardData = Behave.convertJSON(strKeyboardData)

			let timestamps = Behave.timestamps(keyboardData);

			let durations = Behave.durations(keyboardData);

			length = timestamps.length;

			let strMouseData = this.chartData.mouseDataChunk1;

			let mouseData = Behave.convertJSON(strMouseData);


			let leftClickDurations = []
			let rightClickDurations = []
			let doubleClickDurations = []
			let mouseMoveEvents = [] 
			let mouseMoveTimestamps = []

			mouseData.map((el) => {

			  if ("duration" in el) {
				switch (el.event) {
				  case "leftClick": {
					leftClickDurations.push(el.duration);
					break;
				  }

				  case "rightClick" : {
					rightClickDurations.push(el.duration);
					break;
				  }

				  case  "dbclick" : {
					doubleClickDurations.push(el.duration);
					break;
				  }
				}
			  }

			  if (el.event == "mousemove") {
				mouseMoveEvents.push(el);
				mouseMoveTimestamps.push(el.timestamp);
			  }

			});


			//release-to-release time
			if (this.param=="r2r") {
			  values = Behave.releaseToRelease(timestamps);
			  
			}

			// press-to-press time
			if (this.param == "p2p") {
			  values = Behave.pressToPress(timestamps, durations);
			  
			}

			// flight time
			if (this.param == "flight") {
			  values = Behave.flight(timestamps, durations);
			}

			// dwell time
			if (this.param == "dwell") {
			  values = durations;
			}


			// mouse move speed
			if (this.param == "ms") {
			  values = Behave.mouseSpeed(mouseMoveEvents);
			}

			// double click speed
			if (this.param == "dbcs") {
			  values = doubleClickDurations;
			}

			//left click speed
			if (this.param == "lcs") {
			  values = leftClickDurations;
			}

			// right click speed
			if (this.param == "rcs") {
			  values = rightClickDurations;
			}


			let labels = Array(length).fill().map((e,i) => i+1);

			let title = this.title;
			
			this.renderChart({
			  labels: labels,
			  datasets: [
				{
				  label: "Average",
				  backgroundColor: "transparent",
				  data: Array(length).fill(math.mean(values)),
				  borderColor: "#399d39",
				  pointRadius: 0.1,
				},
				{
				  label: 'Value',
				  backgroundColor: 'transparent',
				  pointBackgroundColor: "#0000ff",
				  borderColor: "#0000ff",
				  pointBorderColor: "black",
				  data: values,
				},
			  ],
			}, 
			{
			  title: {
				display: true,
				text: title,
				fontSize: 17
			  },
			  scales : {
				xAxes: [{
				  ticks: {
					max: values.length,
					min: 0,
					autoSkip: true,
					maxRotation: 90,
					minRotation: 90,
					maxTicksLimit: 40
				  }
				}],

				yAxes: [{
				  ticks: {
					max: math.max(values),
					min: math.min(values)
				  }
				}]
			  }
			}
			)
		}
	},
	watch: {
		"chartData": {

			handler: function(old, newVal) {

				this._chart.destroy()
				this.renderChart(this.chartData)

				this.updateChart()
			},
			deep: true
		}
	}

})

</script>