<!-- src/views/UserRegister.vue -->
<template>
  <div class="register">
    <h2>Registrieren</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">Benutzername:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="email">E-Mail:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Passwort:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Registrieren</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { inject } from 'vue';
import AuthService from '../services/auth';
import { useRouter } from 'vue-router';

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
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
    async register() {
      console.log('Registrierung gestartet');
      try {
        const response = await AuthService.register({
          username: this.username,
          email: this.email,
          password: this.password,
        });
        console.log('Registrierung erfolgreich:', response.user);
        // Aktualisieren des Authentifizierungsstatus
        this.auth.isAuthenticated = true;
        // Weiterleitung zur geschützten Route (z.B. Dashboard)
        this.router.push('/dashboard');
      } catch (err) {
        console.error('Fehler bei der Registrierung:', err);
        // Detaillierte Fehlermeldung anzeigen
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message;
        } else {
          this.error = 'Registrierung fehlgeschlagen.';
        }
      }
    },
  },
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: auto;
}
.error {
  color: red;
}
</style>
