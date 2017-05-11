'use strict';

(function($) {
	console.log("init function");


	$.fn.behave = function() {

		var $forms = $("form[data-behave-register], form[data-behave-login]");
		var $registerFormInputs = $("form[data-behave-register] input[type='password'], form[data-behave-login] input[type='password']");
		var keypressQueue = {};
		var passwords = {};
		var isValid = true;
		var currentValue = "";

		$forms.submit(function(e) {
			e.preventDefault();

					    
			if (isValid) {
				var pass_values = []

				for (var i = 0; i<Object.keys(passwords).length; i++) {
					var key_id = "pass" + (i+1);
					pass_values.push(JSON.stringify({type: "keyboard", data: passwords[key_id]}))
				}
			
				$.ajax({
					url: "/jslib",
					type: "POST",
					data: JSON.stringify(pass_values),
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					success: function (data) {
						if (data['status'].toLowerCase() == "success") {
							$(".alert-success").removeClass("hidden");
							$(".alert-danger").addClass("hidden");
						} else {
							$(".alert-success").addClass("hidden");
							$(".alert-danger").removeClass("hidden");
						}
					}
				})
				// console.log(JSON.stringify(pass_values))
			}

		});

		$registerFormInputs.each(function(index, el) {
			$(el).attr("data-passid", index+1);
			var id = "pass" + (index+1);
			passwords[id] = []
		})

		

		$registerFormInputs.keydown(function(event) {
			var timestamp = (new Date).getTime();
			var id = "pass" + $(event.target).attr('data-passid');


			// todo: review needed
			if (event.key.length == 1) 
				keypressQueue[event.keyCode] = timestamp;


			if (event.key.toLowerCase() == "backspace") {
				event.target.value = "";
				keypressQueue = {};
				passwords[id] = []
			}

		});

		$registerFormInputs.keyup(function(event) {
			var timestamp = (new Date).getTime();
			var id = "pass" + $(event.target).attr('data-passid');

			console.log(passwords)

			// todo: review needed
			if (event.key.length==1) {

				var obj = {
					keyPress : keypressQueue[event.keyCode],
					keyRelease : timestamp,
					keyCode : String.fromCharCode(event.keyCode),

				}

				passwords[id].push(obj);

			}

		});
	}
})(jQuery);