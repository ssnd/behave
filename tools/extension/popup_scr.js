$(function(){

	$("#result").hide()

	keydown_timestamp = 0

	data_array = []

	$(".s-input").on("keydown", function(e){
		keydown_timestamp = + new Date()
	})

	$(".s-input").on("keyup", function(e){
		keyup_timestamp = + new Date()

		data_array.push({
			"key_press": keydown_timestamp,
			"key_release": keyup_timestamp
		})
	})

	$("#s-submit").click(function(){
		chrome.storage.sync.set({'user_data': data_array}, function() {
			$("#handler").hide()
			$("#result").show()
		})
	})
})