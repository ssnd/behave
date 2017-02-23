import math from "mathjs";

export default {
	convertJSON(str) {
		return JSON.parse(str);
	},


	// keyboard
	timestamps(arr) {
		let timestamps = arr.map((el) => {
			return el.timestamp;
		})

		return timestamps;
	},

	durations(arr) {
		let durations = arr.map((el) => {
			return el.key_duration;
		})

		return durations;
	},

	flight(timestamps, durations)  {
		let delays = [];

		for (var i = 1; i < timestamps.length-1; i++) {
			let prevRelease = timestamps[i];
			let nextPress = timestamps[i+1] - durations[i+1]
			let flightTime = nextPress - prevRelease

			delays.push(flightTime);
		}

		return delays
	},

	releaseToRelease(timestamps) {
		let delays = Array();

		for (var i = 1; i<timestamps.length-1; i++) {
			let prevRelease = timestamps[i];
			let nextRelease = timestamps[i+1];

			let releaseToRelease = nextRelease - prevRelease

			delays.push(releaseToRelease)

		}

		return delays;
	},

	pressToPress(timestamps, durations) {
		let delays = Array();

		for (var i=1; i<timestamps.length-1; i++) {
			let prevPress = timestamps[i] - durations[i];
			let nextPress = timestamps[i+1] - durations[i+1];

			let pressToPress = nextPress - prevPress;

			delays.push(pressToPress);
		}

		return delays;
	},


	//mouse 

	vectorLength(x,y) {
		let distance = Math.sqrt( Math.pow(x,2) + Math.pow(y, 2));

		return distance;
	},

	vectorCoords(currentPosition, lastPosition) {
		let x = currentPosition[0] - lastPosition[0];
		let y = currentPosition[1] - lastPosition[1];

		return [x,y];
	},

	mouseSpeed(arr) {
		let speedArr = []

		for (var i=1; i<arr.length-1; i++) {

			let chunk = arr[i]

			try {

				let currentPosition = [chunk.mouseX, chunk.mouseY];

				let lastChunk = arr[i-1];

				let lastPosition = [lastChunk.mouseX, lastChunk.mouseY];

				let vectorCoords = this.vectorCoords(currentPosition, lastPosition);

				let distance = this.vectorLength(vectorCoords[0], vectorCoords[1]);

				let timeDiff = chunk.timestamp-lastChunk.timestamp;

				let speed = distance/timeDiff;

				if (!!speed)
					speedArr.push(speed);
			}

			catch(e) {

				console.log("oops");

				console.log(e);

			}

		}

		return speedArr
	}


}


