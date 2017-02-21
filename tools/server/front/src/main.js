import Vue from 'vue'
import VeeValidate, { Validator } from 'vee-validate'
import VueResource from 'vue-resource'
import routes from './routes'


Vue.use(VeeValidate)
Vue.use(VueResource)



$(function(){

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