'use strict';

(function($) {
	console.log("init function");


	$.fn.behave = function() {

		var $forms = $("form[data-behave-register], form[data-behave-login]");
		var $registerFormInputs = $("form[data-behave-register] input[type='password']");
		var keypressQueue = {};
		var passwords = {};
		var isValid = true;
		var currentValue = "";

		$forms.submit(function(e) {
			e.preventDefault();

			// $registerFormInputs.each(function(index, el) {
			// 	if (index > 0 && el.value != currentValue) 
			// 		isValid = false;
			// 	currentValue = el.value;
			// });
			


			if (isValid) {
				$.ajax({
					url: "/register",
					type: "POST",
					data: JSON.stringify(passwords),
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					success: function() {
						console.log("success");
					}
				})

			}

		});

		$registerFormInputs.each(function(index, el) {
			$(el).attr("data-passid", index+1);
			var id = "pass" + (index+1);
			passwords[id] = []
		})

		

		$registerFormInputs.keydown(function(event) {
			var id = "pass" + $(event.target).attr('data-passid');

			// todo: review needed
			if (event.key.length == 1) 
				keypressQueue[event.keyCode] = event.timeStamp;


			if (event.key.toLowerCase() == "backspace") {
				event.target.value = "";
				keypressQueue = {};
				passwords[id] = []
			}

		});

		$registerFormInputs.keyup(function(event) {
			var id = "pass" + $(event.target).attr('data-passid');

			console.log(passwords)

			// todo: review needed
			if (event.key.length==1) {

				var obj = {
					keyPress : keypressQueue[event.keyCode],
					keyRelease : event.timeStamp,
					keyCode : event.keyCode,

				}

				passwords[id].push(obj);

			}

		});
	}
})(jQuery);