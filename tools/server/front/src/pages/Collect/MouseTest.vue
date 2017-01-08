<template>
	<div id="mouse-test-container">
		<h2 style="text-align:center">Mouse Behaviour Test</h2>
		<div id="mouse-window">
			<div class="mouse-btn" style="top: 15px; left: 15px">Left Click</div>
			<div class="mouse-btn" style="bottom: 15px; right: 15px">Left Click</div>
			<div class="mouse-btn" style="top: 15px; right: 15px">Right Click</div>
			<div class="mouse-btn" style="bottom: 15px; left: 15px">Left Click</div>
			<div class="mouse-btn" style="top: 100px; left: 250px">Right Click</div>
			<div class="mouse-btn" style="top: 270px; left: 300px">Left Click</div>
			<div class="mouse-btn" style="top: 60px; right: 150px">Right Click</div>
			<div class="mouse-btn" style="top: 100px; left: 250px">Double Click</div>
			<div class="mouse-btn" style="top: 270px; left: 300px">Double Click</div>
			<div class="mouse-btn" style="top: 60px; right: 150px">Double Click</div>
		</div>
		<input type="submit" name="submit" id="mouse-push" class="submit" value="Next" v-on:click="pushMouseData"> 
	</div>
</template>
<script>


export default {
	methods: {
		pushMouseData(e){
			e.preventDefault();
			/*sessionStorage.setItem('mouseDataChunk', {
				"coords": coords,
				"clicks": clicks,
				"dbclicks": dbclicks,
				"mousedown": mousedown
			});*/ // FIX THISS!!!!!

			sessionStorage.setItem('mouseDataChunk', {
				"coords": "",
				"clicks": "",
				"dbclicks": "",
				"mousedown": ""
			});

			this.$http.post('http://127.0.0.1:5000/collect', {
				personalData: sessionStorage.getItem('personalData'),
				dataChunk1: sessionStorage.getItem('dataChunk1'),
				dataChunk2: sessionStorage.getItem('dataChunk2'),
				mouseDataChunk: sessionStorage.getItem('mouseDataChunk')
			})
			.then(
				(response) => {
					console.log("POST SUCCESS.");
					window.location.href = "/";
				}, 
				(response) => {
					console.log("POST FAILED.");
				}
			);
		}
	}
}


/*
function mouse_test(){



var coords = [];
var clicks = [];
var dbclicks = [];
var mousedown = [];


document.onmousemove = (e) => {

	var event = e || window.event;

	window.mouseX = event.clientX;

	window.mouseY = event.clientY;

}

// catch rightclicks
document.oncontextmenu = () => {
	let mousedownTime = mousedown[mousedown.length-1].timestamp;

	let eventType ="rightClick";

	let clickTime = +new Date();

	let duration = clickTime - mousedownTime;

	let currentPosition = {
		mouseX :	window.mouseX,
		mouseY :	window.mouseY,
		timestamp:	clickTime,
		event:		eventType,
		duration: 	duration,
	}

	clicks.push(currentPosition);

	return false;

}


//catch leftclicks
document.onclick = (e) => {

	let mousedownTime 	= mousedown[mousedown.length-1].timestamp,
		eventType 		= "leftClick",
		clickTime 		= +new Date(),
		duration 		= clickTime - mousedownTime;

	let currentPosition = {
		mouseX :	window.mouseX,
		mouseY :	window.mouseY,
		timestamp:	clickTime,
		event:		eventType,
		duration: 	duration,
	}

	clicks.push(currentPosition);

}

document.onmousedown = (e) => {
	let currentPosition = {
		mouseX :	window.mouseX,
		mouseY :	window.mouseY,
		timestamp:	+new Date(),
		event:		"mousedown"
	}

	mousedown.push(currentPosition);
}


document.ondblclick = (e) => {

	let clicksLength 	= clicks.length,
		firstClick 		= clicks[clicksLength-2].timestamp,
		secondClick 	= clicks[clicksLength-1].timestamp,
		duration 		= secondClick - firstClick;

	let currentPosition = {
		mouseX: 	window.mouseX,
		mouseY: 	window.mouseY,
		timestamp: 	+new Date(),
		event: 		"dbclick",
		duration: 	duration
	}

	dbclicks.push(currentPosition);

}


var mousemov = () => {

	let currentPosition = {
		mouseX : 	window.mouseX,
		mouseY : 	window.mouseY, 
		timestamp: 	+new Date(),
		event: 		"mousemove"
	}

	if (coords.length > 1) {
		let lastPosition 	= coords[coords.length-1],
			lastXPosition 	= lastPosition.mouseX,
			lastYPosition 	= lastPosition.mouseY,
			notUndefined 	= (window.mouseX != undefined && window.mouseY != undefined),
			notLastPosition	= (window.mouseX != lastXPosition && window.mouseY != lastYPosition);

		if ( notUndefined && notLastPosition ) {
			coords.push(currentPosition);
		}

	} else {

		coords.push(currentPosition);

	}

}

setInterval(mousemov, 100);




var buttons = $("#mouse-window").children();
var btnCount = buttons.length;

buttons.each(function(){$(this).hide()});;

var btnSwitch = function(index){
	if(index < btnCount){
		$(buttons[index]).fadeIn();
		if($(buttons[index]).text().includes("Left")){
			$(buttons[index]).click(function(){
				$(buttons[index]).fadeOut();
				btnSwitch(++index);
			});
		}
		else if($(buttons[index]).text().includes("Right")){
			$(buttons[index]).contextmenu(function(){
				$(buttons[index]).fadeOut();
				btnSwitch(++index);
			});
		}
		else{
			$(buttons[index]).dblclick(function(){
				$(buttons[index]).fadeOut();
				btnSwitch(++index);
			});
		}
	}
	else{
		$("#mouse-window").hide();
		$(".submit").show();
	}
}
btnSwitch(0);

}*/



</script>