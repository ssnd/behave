$(function(){

	$("#result").hide()

	data_array = []

	$(".s-input").on("keydown", function(e){
		keydown_timestamp = + new Date()

		data_array.push({
			"key_press": keydown_timestamp,
			"key_release": keydown_timestamp,
			"keycode": e.keyCode
		})
	})

	$(".s-input").on("keyup", function(e){
		keyup_timestamp = + new Date()

		if(data_array[data_array.length - 1].keycode == e.keyCode){
			data_array[data_array.length - 1].key_release = keyup_timestamp
			console.log(data_array[data_array.length - 1].key_release, e.keyCode)
		}
		else{
			data_array[data_array.length - 2].key_release = keyup_timestamp
			console.log(data_array[data_array.length - 2].key_release, e.keyCode)
		}

	})

	$("#s-submit").click(function(){
		chrome.storage.sync.set({'user_data': data_array}, function() {
			console.log(data_array)
			$("#handler").hide()
			$("#result").show()
		})
	})
})