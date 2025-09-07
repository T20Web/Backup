import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NovaFicha from '../views/NovaFicha.vue'
import MinhasFichas from '../views/MinhasFichas.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/nova', component: NovaFicha },
  { path: '/fichas', component: MinhasFichas },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
