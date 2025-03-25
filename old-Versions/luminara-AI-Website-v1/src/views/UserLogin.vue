<!-- src/views/UserLogin.vue -->
<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="email">E-Mail:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Passwort:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { inject } from 'vue';
import AuthService from '../services/auth';
import { useRouter } from 'vue-router';

export default {
  name: 'UserLogin',
  data() {
    return {
      email: '',
      password: '',
      error: '',
    };
  },
  setup() {
    const auth = inject('auth'); // Zugriff auf das bereitgestellte auth-Objekt
    const router = useRouter();

    return { auth, router };
  },
  methods: {
    async login() {
      console.log('Login gestartet');
      try {
        const response = await AuthService.login({
          email: this.email,
          password: this.password,
        });
        console.log('Login erfolgreich:', response.user);
        // Aktualisieren des Authentifizierungsstatus
        this.auth.isAuthenticated = true;
        // Weiterleitung zur geschützten Route (z.B. Dashboard)
        this.router.push('/dashboard');
      } catch (err) {
        console.error('Fehler beim Login:', err);
        // Detaillierte Fehlermeldung anzeigen
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message;
        } else {
          this.error = 'Login fehlgeschlagen.';
        }
      }
    },
  },
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: auto;
}
.error {
  color: red;
}
</style>
