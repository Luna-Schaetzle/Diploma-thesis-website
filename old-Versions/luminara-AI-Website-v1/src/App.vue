<!-- src/App.vue -->
<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Obere Navbar -->
    <header class="top-navbar">
      <nav>
        <router-link to="/" class="nav-link" exact-active-class="active">Home</router-link>
        <router-link v-if="isAuthenticated" to="/dashboard" class="nav-link" exact-active-class="active">Dashboard</router-link>
        <router-link v-if="isAuthenticated" to="/account" class="nav-link" exact-active-class="active">Account</router-link>
        <router-link v-if="isAuthenticated" to="/applications" class="nav-link" exact-active-class="active">Applications</router-link>
        <router-link v-if="!isAuthenticated" to="/register" class="nav-link" exact-active-class="active">Registrieren</router-link>
        <router-link v-if="!isAuthenticated" to="/login" class="nav-link" exact-active-class="active">Login</router-link>
        <button v-if="isAuthenticated" @click="logout" class="nav-button">Logout</button>
      </nav>
      <!-- Dark Mode Toggle Button in der Top Navbar -->
      <button class="dark-mode-toggle" @click="toggleDarkMode">
        {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
      </button>
    </header>

    <!-- Router View für Hauptansichten -->
    <router-view></router-view>
  </div>
</template>

<script>
import AuthService from './services/auth';

export default {
  name: 'App',
  data() {
    return {
      isDarkMode: false, // Dark Mode Status
      isAuthenticated: AuthService.isAuthenticated(), // Authentifizierungsstatus
    };
  },
// In den Methoden von App.vue
methods: {
  toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;
    localStorage.setItem('isDarkMode', this.isDarkMode);
  },
  logout() {
    AuthService.logout();
    this.isAuthenticated = false;
    this.$router.push('/login');
    // Event-Emitter
    this.$emit('auth-status-changed', false);
  },
  updateAuthStatus(status) {
    this.isAuthenticated = status;
  },
},
/*
created() {
  // ...
  this.$on('auth-status-changed', this.updateAuthStatus);
},
beforeUnmount() {
  this.$off('auth-status-changed', this.updateAuthStatus);
},
*/
};


</script>

<style scoped>
/* Grundlegende Stile für die App */
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  color: #333;
  min-height: 100vh;
  display: flex;
  flex-direction: column; /* column für die Top Navbar */
  transition: background-color 0.3s, color 0.3s;
}

/* Dark Mode Stile */
#app.dark-mode {
  background-color: #121212;
  color: #f0f0f0;
}

/* Obere Navbar */
.top-navbar {
  width: 100%;
  background-color: #ffffff;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s, box-shadow 0.3s;
}

#app.dark-mode .top-navbar {
  background-color: #1e1e1e;
  box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
}

.top-navbar nav {
  display: flex;
  gap: 15px;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-link:hover {
  background-color: #f0f0f0;
}

.active {
  background-color: #3498db;
  color: white;
}

#app.dark-mode .nav-link {
  color: #f0f0f0;
}

#app.dark-mode .nav-link:hover {
  background-color: #2c2c2c;
}

#app.dark-mode .active {
  background-color: #2ecc71;
}

/* Dark Mode Toggle Button innerhalb der Top Navbar */
.dark-mode-toggle {
  background-color: #20c997;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.dark-mode-toggle:hover {
  background-color: #1aa179;
}

.dark-mode-toggle:active {
  transform: scale(0.98);
}

#app.dark-mode .dark-mode-toggle {
  background-color: #bb86fc;
}

#app.dark-mode .dark-mode-toggle:hover {
  background-color: #985eff;
}

/* Responsive Anpassungen für die Top Navbar */
@media (max-width: 900px) {
  .top-navbar nav {
    flex-wrap: wrap;
    gap: 10px;
  }
}
/* Stile für die Navbar und Buttons */

.top-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #3498db;
}

.nav-link {
  margin-right: 15px;
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-link.active {
  text-decoration: underline;
}

.nav-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.nav-button:hover {
  background-color: #c0392b;
}

.dark-mode-toggle {
  background-color: transparent;
  border: 2px solid white;
  color: white;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.dark-mode-toggle:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.dark-mode {
  background-color: #121212;
  color: #f0f0f0;
}

/* Weitere Stile nach Bedarf */
</style>
