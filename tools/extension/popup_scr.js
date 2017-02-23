$(function(){
	$("#result").hide()

	data_obj = {"p1": [], "p2": [], "p3": [], "p4": []}

	$(".s-input").on("keydown", function(e){

		let data_array = data_obj[$(this).attr('id')]

		keydown_timestamp = + new Date()
		if(e.keyCode == 8){
			data_obj[$(this).attr('id')] = []
			$(this).val("")
			return;
		}
		data_array.push({
			"key_press": keydown_timestamp,
			"key_release": keydown_timestamp,
			"keycode": e.keyCode
		})

		data_obj[$(this).attr('id')] = data_array
	})

	$(".s-input").on("keyup", function(e){

		let data_array = data_obj[$(this).attr('id')]

		keyup_timestamp = + new Date()
		if(data_array[data_array.length - 1].keycode == e.keyCode){
			data_array[data_array.length - 1].key_release = keyup_timestamp
		}
		else if(data_array.length > 1){
			data_array[data_array.length - 2].key_release = keyup_timestamp
		}
		else{
			data_array[data_array.length - 1].key_release = keyup_timestamps
		}

		data_obj[$(this).attr('id')] = data_array

	})
	$("#s-submit").click(function(){
		if($("#p1").val() == $("#p2").val() && $("#p1").val() == $("#p3").val() && $("#p1").val() == $("#p4").val()){
		chrome.storage.local.set({'user_data': JSON.stringify(data_obj), 
			'user_pass': md5($("#p1").val(), null, true)}, function() {
			console.log(data_obj)
			$("#handler").hide()
			$("#result").show()
		})
		}
		else{
			alert("All the passwords must be equal")
		}
	})
})