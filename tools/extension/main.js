console.log("~BEHAVE")


function normalize_data(user_data){
	dwellTime = []
	//flightTime = []

	for(var i = 1; i < user_data.length; i++){
		dwellVal = user_data[i].key_release - user_data[i].key_press
	//	flightVal = user_data[i].key_press - user_data[i-1].key_release

		if(dwellVal > 2) dwellTime.push(dwellVal)

	//	flightTime.push(flightVal)
	}
	/*flightTime_f1 = []
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
	console.log(flightTime_f2)*/
	return {"dwellTime": dwellTime}
}

keydown_timestamp = 0

data_array = []

$("#pass").on("keydown", function(e){
	keydown_timestamp = + new Date()

	data_array.push({
		"key_press": keydown_timestamp,
		"key_release": keydown_timestamp,
		"keycode": e.keyCode
	})
})

$("#pass").on("keyup", function(e){
	keyup_timestamp = + new Date()

	if(data_array[data_array.length - 1].keycode == e.keyCode){
		data_array[data_array.length - 1].key_release = keyup_timestamp
		//console.log(data_array[data_array.length - 1].key_release, e.keyCode)
	}
	else{
		data_array[data_array.length - 2].key_release = keyup_timestamp
		//console.log(data_array[data_array.length - 2].key_release, e.keyCode)
	}

})


secureState = false

$("#login_form").on('submit', function(e){

	//if(!secureState){s

	chrome.storage.sync.get(function (obj) {
	    userData = obj.user_data

	    if(userData.length < 2 || data_array.length < 2){
	    	console.log("Too few typing data")
	    	return;
	    }
	   	reservedData = normalize_data(userData)

	    clientData = normalize_data(data_array)

	    //console.log("R", reservedData)
	    //console.log("c", clientData)

	   	reservedDwellAvg = math.mean(reservedData.dwellTime)
	   	reservedDwellStd = math.std(reservedData.dwellTime)

	   	clientDwellAvg = math.mean(clientData.dwellTime)
	   	clientDwellStd = math.std(clientData.dwellTime)

	   	console.log(reservedDwellAvg, reservedDwellStd)
	   	console.log(clientDwellAvg, clientDwellStd)


		maxDwellDeltaAvg = reservedDwellAvg / 6
		maxDwellDeltaStd = reservedDwellStd / 3

		console.log(maxDwellDeltaAvg, maxDwellDeltaStd)


		if(Math.abs(reservedDwellAvg - clientDwellAvg) < maxDwellDeltaAvg && Math.abs(reservedDwellStd - clientDwellStd) < maxDwellDeltaStd){
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