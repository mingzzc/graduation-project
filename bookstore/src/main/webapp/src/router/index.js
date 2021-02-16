import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import Welcome from '../components/Welcome.vue'
import Book from '../components/Book.vue'
import Search from '../components/Search.vue'
import Recommend from '../components/Recommend.vue'
import Tag from '../components/Tag.vue'
import Admin from '../components/Admin.vue'


Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/welcome' },
  {
    path: '/home',
      component: Home,
      children:[
        { path: '/welcome', component: Welcome },
        { path: '/book/:id', component: Book },
        { path: '/search/:key', component: Search },
        { path: '/recommend',component: Recommend },
        { path: '/tag',component:Tag }
      ]
  },
  {path: '/admin', component: Admin}
]

const router = new VueRouter({
  routes
})

export default router
