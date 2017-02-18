console.log("~BEHAVE")


function normalize_data(user_data){
	dwellTime = []
	flightTime = []

	for(var i = 1; i < user_data.length; i++){
		dwellVal = user_data[i].key_release - user_data[i].key_press
		flightVal = user_data[i].key_press - user_data[i-1].key_release

		dwellTime.push(dwellVal)

		flightTime.push(flightVal)
	}
	flightTime_f1 = []
	for(var i = 0; i < flightTime.length; i++){
		if(flightTime[i] > 5){
			flightTime_f1.push(flightTime[i])
		}
	}
	flightSTD = math.std(flightTime_f1)

	flightTime_f2 = []
	for(var i = 0; i < flightTime_f1.length; i++){
		if(flightTime_f1[i] < flightSTD * 2){
			flightTime_f2.push(flightTime_f1[i])
		}
	}
	console.log(flightTime_f2)
	return {"dwellTime": dwellTime, "flightTime": flightTime_f2}
}

keydown_timestamp = 0

data_array = []

$("#email").on("keydown", function(e){
	keydown_timestamp = + new Date()
})

$("#email").on("keyup", function(e){
	keyup_timestamp = + new Date()

	data_array.push({
		"key_press": keydown_timestamp,
		"key_release": keyup_timestamp
	})
})

$("#pass").on("keydown", function(e){
	keydown_timestamp = + new Date()
})

$("#pass").on("keyup", function(e){
	keyup_timestamp = + new Date()

	data_array.push({
		"key_press": keydown_timestamp,
		"key_release": keyup_timestamp
	})
})

secureState = false

$("#login_form").on('submit', function(e){

	//if(!secureState){
	
	

	chrome.storage.sync.get(function (obj) {
	    userData = obj.user_data

	    clientData = normalize_data(data_array)

	   	reservedData = normalize_data(userData)

	   	reservedDwellAvg = math.mean(reservedData.dwellTime)
	   	reservedFlightAvg = math.mean(reservedData.flightTime)

	   	clientDwellAvg = math.mean(clientData.dwellTime)
	   	clientFlightAvg = math.mean(clientData.flightTime)

		console.log(clientFlightAvg, clientDwellAvg)

		console.log(reservedFlightAvg, reservedDwellAvg)


		maxFlightDelta = 20
		maxDwellDelta = 15


		if(Math.abs(reservedFlightAvg - clientFlightAvg) < maxFlightDelta && Math.abs(reservedDwellAvg - clientDwellAvg) < maxDwellDelta){
			secureState = true
		}
		else{
			secureState = false
		}

		console.log(secureState)

		if(secureState){
			console.log("Behave test success.")
		}
		else{
			e.preventDefault()
			alert("Behave security test failed.")
			location.reload()
		}

	})
	//}

})