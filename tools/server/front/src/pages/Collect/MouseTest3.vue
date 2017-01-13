<template>
	<div id="mouse-test-container">
		<h2 style="text-align:center">Mouse Behaviour Test 3</h2>
		<div id="mouse-window">
			<div data-event="left" class="mouse-btn" style="top: 15px; left: 15px">Left Click</div>
			<div data-event="left" class="mouse-btn" style="bottom: 15px; right: 15px">Left Click</div>
			<div data-event="right" class="mouse-btn" style="top: 15px; right: 15px">Right Click</div>
			<div data-event="left" class="mouse-btn" style="bottom: 15px; left: 15px">Left Click</div>
			<div data-event="right" class="mouse-btn" style="top: 100px; left: 250px">Right Click</div>
			<div data-event="left" class="mouse-btn" style="top: 270px; left: 300px">Left Click</div>
			<div data-event="right" class="mouse-btn" style="top: 60px; right: 150px">Right Click</div>
			<div data-event="double" class="mouse-btn" style="top: 100px; left: 250px">Double Click</div>
			<div data-event="double" class="mouse-btn" style="top: 270px; left: 300px">Double Click</div>
			<div data-event="double" class="mouse-btn" style="top: 60px; right: 150px">Double Click</div>
			<div data-event="left" class="mouse-btn" style="top: 15px; left: 15px">Left Click</div>
			<div data-event="left" class="mouse-btn" style="bottom: 150px; right: 15px">Left Click</div>
			<div data-event="right" class="mouse-btn" style="top: 150px; right: 15px">Right Click</div>
			<div data-event="left" class="mouse-btn" style="bottom: 15px; left: 15px">Left Click</div>
			<div data-event="right" class="mouse-btn" style="top: 100px; left: 250px">Right Click</div>
			<div data-event="left" class="mouse-btn" style="top: 270px; left: 300px">Left Click</div>
			<div data-event="right" class="mouse-btn" style="top: 60px; right: 150px">Right Click</div>
			<div data-event="double" class="mouse-btn" style="top: 200px; left: 350px">Double Click</div>
			<div data-event="double" class="mouse-btn" style="top: 170px; left: 200px">Double Click</div>
			<div data-event="double" class="mouse-btn" style="top: 60px; right: 150px">Double Click</div>
		</div>
		<input type="submit" name="submit" id="mouse-push" class="submit" value="Next" v-on:click="pushMouseData"> 
	</div>
</template>
<script>


export default {
	mounted: function() {

		this.collectMouseData();

		this.mouseTestInit();

	},

	data() {
		return {
			coords : [],
			clicks : [],
			dbclicks : [],
			mousedown: []
		}
	},
	methods: {
		nextButton(buttons, index) {

			let button = buttons.eq(index);

			button.fadeOut();

			this.startMouseTest(++index, buttons);

		},

		startMouseTest(index, buttons) {
			let btnCount = buttons.length;

			let obj = this;

			if(index < btnCount){

				let button = $(buttons[index]);

				let event_type = button.attr("data-event");

				button.fadeIn();

				switch (event_type) {
					case "left" : {
						button.click(function() {
							obj.nextButton(buttons, index)
						})
					}

					case "right" : {
						button.contextmenu(function(){
							obj.nextButton(buttons, index)
						});
					}

					case "double" : {
						button.dblclick(function(){
							obj.nextButton(buttons, index)
						});
					}
				}
			} else {

				$("#mouse-window").hide();
				$(".submit").show();

			}
		},

		mouseTestInit() {

			var buttons = $("#mouse-window").children();

			let btnCount = buttons.length;

			buttons.hide();

			this.startMouseTest(0, buttons);

		},

		onMouseDown(e) {

			let currentPosition = {
				mouseX :		window.mouseX,
				mouseY :		window.mouseY,
				timestamp:	+new Date(),
				event:			"mousedown"
			}

			this.mousedown.push(currentPosition);

		},

		onContextMenu(e) {
			e.preventDefault()
			let mousedownTime = this.mousedown[this.mousedown.length-1].timestamp;

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

			this.clicks.push(currentPosition);

			return false;
		},

		onClick(e) {
			let mousedownTime		= this.mousedown[this.mousedown.length-1].timestamp,
					event_type			= "leftClick",
					clickTime				= +new Date(),
					duration				= clickTime - mousedownTime;

			let currentPosition = {
				mouseX		:		window.mouseX,
				mouseY		:		window.mouseY,
				timestamp	:		clickTime,
				event		:		"leftClick",
				duration	:		duration,
			}

			this.clicks.push(currentPosition);

		},

		onDbClick(e) {

			let clicksLength 		= this.clicks.length,
				firstClick 				= this.clicks[clicksLength-2].timestamp,
				secondClick 			= this.clicks[clicksLength-1].timestamp,
				duration 					= secondClick - firstClick;

			let currentPosition = {
				mouseX: 			window.mouseX,
				mouseY: 			window.mouseY,
				timestamp: 		+new Date(),
				event: 				"dbclick",
				duration: 		duration
			}

			this.dbclicks.push(currentPosition);

		},

		mouseCoordsHandle(e) {

			var event = e || window.event;

			window.mouseX = event.clientX;

			window.mouseY = event.clientY;

		},

		onMouseMove() {
			let currentPosition = {
				mouseX:		window.mouseX,
				mouseY:		window.mouseY, 
				timestamp:	+new Date(),
				event:			"mousemove"
			}

			if (this.coords.length > 1) {
				let lastPosition 		= this.coords[this.coords.length-1],
						lastXPosition 	= lastPosition.mouseX,
						lastYPosition 	= lastPosition.mouseY,
						notUndefined 		= (window.mouseX != undefined && window.mouseY != undefined),
						notLastPosition	= (window.mouseX != lastXPosition && window.mouseY != lastYPosition);

				if ( notUndefined && notLastPosition ) {

					this.coords.push(currentPosition);
				}

			} else {

				this.coords.push(currentPosition);

			}

		},

		collectMouseData() {
			// on mouse move
			document.onmousemove = this.mouseCoordsHandle;

			document.onmousedown = (e) => {
				this.onMouseDown(e);

				document.oncontextmenu = this.onContextMenu;
				document.onclick = this.onClick;
			}

			document.ondblclick = this.onDbClick;

			setInterval(this.onMouseMove, 100);
		},


		pushMouseData(e){
			e.preventDefault();

			let final_array = this.coords.concat(this.clicks , this.dbclicks);

			final_array.sort((x,y) =>  {
				return x.timestamp-y.timestamp
			})

			let jsonData = JSON.stringify(final_array)
			sessionStorage.setItem('mouseDataChunk3', jsonData);

			this.$parent._data.currentView = "MouseTest4";
		}
	}
}



</script>