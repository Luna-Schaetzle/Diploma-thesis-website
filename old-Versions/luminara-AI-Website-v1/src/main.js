// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import AuthService from './services/auth';

const app = createApp(App);

// Axios konfigurieren
axios.defaults.baseURL = 'http://localhost:5000/api';

// Interceptor hinzufügen
axios.interceptors.request.use(
    config => {
        const token = AuthService.getToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

app.use(router);
app.mount('#app');
