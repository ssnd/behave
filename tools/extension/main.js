console.log("~BEHAVE")

function normalize_data(user_data){
	dwellTime = []
	flightTime = []
	rtor = []
	ptop = []


	for(var i = 1; i < user_data.length; i++){
		flightTime.push(user_data[i].key_press - user_data[i-1].key_release)
		rtor.push(user_data[i].key_release - user_data[i-1].key_release)
		ptop.push(user_data[i].key_press - user_data[i-1].key_press)

		dwellVal = user_data[i].key_release - user_data[i].key_press
		if(dwellVal > 2) dwellTime.push(dwellVal)

	}
	console.log(rtor, ptop)


	flightTime_f1 = []
	rtor_f1 = []
	ptop_f1 = []
	for(var i = 0; i < flightTime.length; i++){
		if(flightTime[i] < math.mean(flightTime) + math.std(flightTime) && flightTime[i] > 10){
			flightTime_f1.push(flightTime[i])
		}
		if(rtor[i] < math.mean(rtor) + math.std(rtor) && rtor[i] > 5){
			rtor_f1.push(rtor[i])
		}
		if(ptop[i] < math.mean(ptop) + math.std(ptop) && ptop[i] > 5){
			ptop_f1.push(ptop[i])
		}
	}
	console.log(rtor_f1, ptop_f1)
	return {"dwellTime": dwellTime, "flightTime": flightTime_f1, "rtor": rtor_f1, "ptop": ptop_f1}
}

keydown_timestamp = 0

data_array = []

$("#pass").on("keydown", function(e){
	keydown_timestamp = + new Date()
	if(e.keyCode == 8){
		data_array = data_array.slice(0, data_array.length - ($(this).val()).length)
		$(this).val("")
		return;
	}
	data_array.push({
		"key_press": keydown_timestamp,
		"key_release": keydown_timestamp,
		"keycode": e.keyCode
	})
})

$("#pass").on("keyup", function(e){
	keyup_timestamp = + new Date()
	if(e.keyCode == 8){return;}
	if(data_array[data_array.length - 1].keycode == e.keyCode){
		data_array[data_array.length - 1].key_release = keyup_timestamp
	}
	else if(data_array.length > 1){
		data_array[data_array.length - 2].key_release = keyup_timestamp
	}
	else{
		data_array[data_array.length - 1].key_release = keyup_timestamp
	}

})


secureState = false

$("#login_form").on('submit', function(e){

	//if(!secureState){s

	chrome.storage.local.get(function (obj) {
		if(md5($("#pass").val(), null, true) != obj.user_pass){
			e.preventDefault()
			alert("Behave: Entered password is wrong")
			location.reload()
			return;
		}
		reservedDataStack = Object.values(JSON.parse(obj.user_data))

		reservedParams = [ [], [], [], [] ]
		for(let i = 0; i < reservedDataStack.length; i++){
			reservedData = normalize_data(reservedDataStack[i])

			let reservedDwellAvg = math.mean(reservedData.dwellTime)
			let reservedFlightAvg = math.mean(reservedData.flightTime)
			let reservedRtorAvg = math.mean(reservedData.rtor)
			let reservedPtopAvg = math.mean(reservedData.ptop)

			reservedParams[0].push(reservedDwellAvg)
			reservedParams[1].push(reservedFlightAvg)
			reservedParams[2].push(reservedRtorAvg)
			reservedParams[3].push(reservedPtopAvg)
		}
		
		if(data_array.length < 2){
			e.preventDefault()
			alert("Behave: Too few typing data")
			location.reload()
			return;
		}

		clientData = normalize_data(data_array)

		clientDwellAvg = math.mean(clientData.dwellTime)
		clientFlightAvg = math.mean(clientData.flightTime)
		clientRtorAvg = math.mean(clientData.rtor)
		clientPtopAvg = math.mean(clientData.ptop)

		console.log(clientData.rtor, clientData.ptop)

		reservedDwellAvg = math.mean(reservedParams[0])
		reservedFlightAvg = math.mean(reservedParams[1])
		reservedRtorAvg = math.mean(reservedParams[2])
		reservedPtopAvg = math.mean(reservedParams[3])

		console.log("RESERVED: ", reservedDwellAvg, reservedFlightAvg, reservedRtorAvg, reservedPtopAvg)
		console.log("CLIENT: ", clientDwellAvg, clientFlightAvg, clientRtorAvg, clientPtopAvg)

		maxDwellAvgDiff = reservedDwellAvg / 7
		maxFlightAvgDiff = reservedFlightAvg / 4
		maxRtorAvgDiff = reservedRtorAvg / 6
		maxPtopAvgDiff = reservedPtopAvg / 6


		dwellAvgDiff = Math.abs(clientDwellAvg - reservedDwellAvg)
		flightAvgDiff = Math.abs(clientFlightAvg - reservedFlightAvg)
		rtorAvgDiff = Math.abs(clientRtorAvg - reservedRtorAvg)
		ptopAvgDiff = Math.abs(clientPtopAvg - reservedPtopAvg)

		console.log("DIFF: ", dwellAvgDiff, flightAvgDiff, rtorAvgDiff, ptopAvgDiff)

		console.log("DELTAS: ", maxDwellAvgDiff, maxFlightAvgDiff, maxRtorAvgDiff, maxPtopAvgDiff)

		if(dwellAvgDiff < maxDwellAvgDiff
			&& flightAvgDiff < maxFlightAvgDiff
			&& rtorAvgDiff < maxRtorAvgDiff
			&& ptopAvgDiff < maxPtopAvgDiff){

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
			alert("Behave: Security test failed.")
			location.reload()
		}

	}) 
	//}

})