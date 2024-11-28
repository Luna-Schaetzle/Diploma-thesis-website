// src/router.js

// Importiere weitere Komponenten wie Register.vue, Login.vue, etc.

// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, getDoc } from 'firebase/firestore';

// Importieren Sie Ihre Hauptansichten
import HomeView from '../src/views/HomeView.vue';
import DashboardView from '../src/views/DashboardView.vue';
import AccountView from '../src/views/AccountView.vue';
import ApplicationsView from '../src/views/ApplicationsView.vue';
import OCRView from '../src/views/OCRView.vue';
import OpenAIImage from '../src/views/OpenAIImage.vue';

// Importieren Sie die Sidebar-Komponenten als Unterrouten
import LuminaraOllama from '../src/components/LuminaraOllama.vue';
import LuminaraImage from '../src/components/LuminaraImage.vue';
import LuminaraGallery from '../src/components/LuminaraGallery.vue';
import ChatGPT from '../src/components/ChatGPTComponent.vue';
import LuminaraVision from '../src/components/LuminaraVision.vue';
import LuminaraCode from '../src/components/LuminaraCode.vue';

import LoginComponent from "../src/components/LoginComponent";
import RegisterComponent from "../src/components/RegisterComponent";
//import { meta } from '@babel/eslint-parser';

import AdminDashboard from '../src/views/AdminDashboard.vue';
import ApplicationDetails from '../src/components/ApplicationDetails.vue';


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
      {
        path: 'vision',
        name: 'LuminaraVision',
        component: LuminaraVision,
      },
      {
        path: 'code',
        name: 'LuminaraCode',
        component: LuminaraCode,
      },
    ],
  },
  { path: '/ocr', name: 'OCR', component: OCRView },
  { path: '/openaiimage', name: 'openaiimage', component: OpenAIImage },
  { path: "/login", name: "Login", component: LoginComponent },
  { path: "/register", name: "Register", component: RegisterComponent },
  { path: '/admin', component: AdminDashboard, meta: { requiresAdmin: true } },
  { path: '/admin/applications/:id', component: ApplicationDetails, meta: { requiresAdmin: true } },
];

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


// Navigation Guard für Admin-Routen
router.beforeEach(async (to, from, next) => {
  const auth = getAuth();
  const currentUser = auth.currentUser;

  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (currentUser) {
      const db = getFirestore();
      const userRef = doc(db, "users", currentUser.uid);
      try {
        const userDoc = await getDoc(userRef);
        if (userDoc.exists()) {
          const userData = userDoc.data();
          if (userData.role === 'admin') {
            next();
          } else {
            next('/account'); // Weiterleitung zu Account-Dashboard
          }
        } else {
          next('/login');
        }
      } catch (error) {
        next('/login');
      }
    } else {
      next('/login');
    }
  } else {
    next();
  }
});

export default router;
