import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import HomePage from '../views/Login.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/cavelist',
    name: 'CaveList',
    component: () => import('@/views/CaveList.vue')
  },
  {
    path: '/cave',
    name: 'Cave',
    component: () => import('@/views/Cave.vue')
  },
  {
    path: '/newBottle',
    name: 'AddBottle',
    component: () => import('@/views/AddBottle.vue')
  },
  {
    path: '/historique',
    name: 'Historique',
    component: () => import('@/views/Historique.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
