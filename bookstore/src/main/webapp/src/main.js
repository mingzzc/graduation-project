import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import axios from 'axios'


Vue.config.productionTip = false

Vue.prototype.$http = axios
//配置请求的根路径
axios.defaults.baseURL = "http://127.0.0.1:8888/"

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
