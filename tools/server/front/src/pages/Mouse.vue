
<template>

</template>

<script>

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

window.onload = () => {
	setInterval(mousemov, 100);
}


</script>

<style>

</style>