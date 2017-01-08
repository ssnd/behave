import Vue from 'vue'
import VeeValidate from 'vee-validate'
import VueResource from 'vue-resource'
import routes from './routes'


Vue.use(VeeValidate)
Vue.use(VueResource)



$(function(){


function mouse_test(){



console.log("ddd");
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
    mouseX :  window.mouseX,
    mouseY :  window.mouseY,
    timestamp:  clickTime,
    event:    eventType,
    duration:   duration,
  }

  clicks.push(currentPosition);

  return false;

}


//catch leftclicks
document.onclick = (e) => {

  let mousedownTime   = mousedown[mousedown.length-1].timestamp,
    eventType     = "leftClick",
    clickTime     = +new Date(),
    duration    = clickTime - mousedownTime;

  let currentPosition = {
    mouseX :  window.mouseX,
    mouseY :  window.mouseY,
    timestamp:  clickTime,
    event:    eventType,
    duration:   duration,
  }

  clicks.push(currentPosition);

}

document.onmousedown = (e) => {
  let currentPosition = {
    mouseX :  window.mouseX,
    mouseY :  window.mouseY,
    timestamp:  +new Date(),
    event:    "mousedown"
  }

  mousedown.push(currentPosition);
}


document.ondblclick = (e) => {

  let clicksLength  = clicks.length,
    firstClick    = clicks[clicksLength-2].timestamp,
    secondClick   = clicks[clicksLength-1].timestamp,
    duration    = secondClick - firstClick;

  let currentPosition = {
    mouseX:   window.mouseX,
    mouseY:   window.mouseY,
    timestamp:  +new Date(),
    event:    "dbclick",
    duration:   duration
  }

  dbclicks.push(currentPosition);

}


var mousemov = () => {

  let currentPosition = {
    mouseX :  window.mouseX,
    mouseY :  window.mouseY, 
    timestamp:  +new Date(),
    event:    "mousemove"
  }

  if (coords.length > 1) {
    let lastPosition  = coords[coords.length-1],
      lastXPosition   = lastPosition.mouseX,
      lastYPosition   = lastPosition.mouseY,
      notUndefined  = (window.mouseX != undefined && window.mouseY != undefined),
      notLastPosition = (window.mouseX != lastXPosition && window.mouseY != lastYPosition);

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

}



const app = new Vue({
  el: '#app',
  data: {
    currentRoute: window.location.pathname,
  },
  computed: {
    ViewComponent () {
      const matchingView = routes[this.currentRoute]
      return matchingView
        ? require('./pages/' + matchingView + '.vue')
        : require('./pages/404.vue')
    }
  },
  render (h) {
    return h(this.ViewComponent)
  }
})

window.addEventListener('popstate', () => {
  app.currentRoute = window.location.pathname
})
});