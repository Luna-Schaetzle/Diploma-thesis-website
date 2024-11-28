// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';

// Importieren Sie Ihre Hauptansichten
import HomeView from '../views/HomeView.vue';
import DashboardView from '../views/DashboardView.vue';
import AccountView from '../views/AccountView.vue';
import ApplicationsView from '../views/ApplicationsView.vue';
import OCRView from '../views/OCRView.vue';


// Importieren Sie die Sidebar-Komponenten als Unterrouten
import LuminaraOllama from '../components/LuminaraOllama.vue';
import OllamaChat from '../components/OllamaChat.vue';
import LuminaraImage from '../components/LuminaraImage.vue';
import LuminaraGallery from '../components/LuminaraGallery.vue';
import ChatGPT from '../components/ChatGPTComponent.vue';
import OpenAIImage from '../views/OpenAIImage.vue';

import LoginComponent from "@/components/LoginComponent";
import RegisterComponent from "@/components/RegisterComponent";
//import { meta } from '@babel/eslint-parser';

// Definiere die Routen
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
    meta: { requiresAuth: true }, // Auth erforderlich
  },
  {
    path: '/account',
    name: 'Account',
    component: AccountView,
    meta: { requiresAuth: true }, // Auth erforderlich
  },
  {
    path: '/applications',
    name: 'Applications',
    component: ApplicationsView,
    meta: { requiresAuth: true }, // Auth erforderlich
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
  { path: '/ocr', name: 'OCR', component: OCRView },
  {
    path: "/openaiimage", // Der Pfad, der aufgerufen wird
    name: "OpenAIImage",
    component: OpenAIImage, // Die Komponente, die bei diesem Pfad geladen wird
    meta: { requiresAuth: true }, // Auth erforderlich
  },
  { path: "/login", name: "Login", component: LoginComponent },
  { path: "/register", name: "Register", component: RegisterComponent },
];

// Erstelle den Router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard für Authentifizierungsprüfung
router.beforeEach((to, from, next) => {
  const auth = getAuth();
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth) {
    // Überprüfen, ob Benutzer eingeloggt ist
    onAuthStateChanged(auth, (user) => {
      if (user) {
        // Benutzer ist eingeloggt
        next();
      } else {
        // Benutzer ist nicht eingeloggt, umleiten zu Login
        next({ path: "/login" });
      }
    });
  } else {
    // Keine Authentifizierung erforderlich
    next();
  }
});

export default router;
