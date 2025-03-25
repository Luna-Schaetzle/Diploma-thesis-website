// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import DashboardView from '../views/DashboardView.vue';
import UserProfile from '../views/UserProfile.vue'; // Korrekte Datei
import ApplicationsView from '../views/ApplicationsView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue';

import AuthService from '../services/auth';

// Importieren Sie die Sidebar-Komponenten als Unterrouten
import LuminaraOllama from '../components/LuminaraOllama.vue';
import OllamaChat from '../components/OllamaChat.vue';
import LuminaraImage from '../components/LuminaraImage.vue';
import LuminaraGallery from '../components/LuminaraGallery.vue';
import ChatGPT from '../components/ChatGPTComponent.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/account',
    name: 'Account',
    component: UserProfile, // Korrekte Referenz
    meta: { requiresAuth: true },
  },
  {
    path: '/applications',
    name: 'Applications',
    component: ApplicationsView,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'ollama',
        name: 'LuminaraOllama',
        component: LuminaraOllama,
      },
      {
        path: 'chat',
        name: 'OllamaChat',
        component: OllamaChat,
      },
      {
        path: 'image',
        name: 'LuminaraImage',
        component: LuminaraImage,
      },
      {
        path: 'gallery',
        name: 'LuminaraGallery',
        component: LuminaraGallery,
      },
        {
        path: 'chatgpt',
        name: 'ChatGPT',
        component: ChatGPT,
        },
    ],
  },
  {
    path: '/register',
    name: 'UserRegister', // Korrekte Referenz
    component: UserRegister, // Korrekte Referenz
  },
  {
    path: '/login',
    name: 'UserLogin', // Korrekte Referenz
    component: UserLogin, // Korrekte Referenz
  },
  // Weitere Routen...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !AuthService.isAuthenticated()) {
    next('/login');
  } else {
    next();
  }
});

export default router;