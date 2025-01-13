<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Obere Navbar -->
    <header class="top-navbar">
      <nav>
        <router-link to="/" class="nav-link" exact-active-class="active">Home</router-link>
        <router-link v-if="user" to="/account" class="nav-link" exact-active-class="active">Account</router-link>
        <router-link v-if="user" to="/applications" class="nav-link" exact-active-class="active">Chat Bots</router-link>
        <router-link v-if="user" to="/ocr" class="nav-link" exact-active-class="active">OCR</router-link>
        <router-link v-if="user" to="/openaiimage" class="nav-link" exact-active-class="active">OpenAI Image</router-link>
        
      </nav>

      <!-- Login/Logout/Registrierung Buttons -->
      <div class="auth-button-group">
        <button v-if="!user" @click="goToLogin" class="auth-button">Login</button>
        <button v-if="!user" @click="goToRegister" class="auth-button">Register</button>
        <button v-if="user" @click="logout" class="auth-button">Logout</button>
      </div>
    </header>

    <!-- Router View für Hauptansichten -->
    <router-view></router-view>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
      <p>AI can make mistakes, please use with caution, and always double-check the results.</p>
      &copy; 2024 Luminara AI-Student-Plattform | All Rights Reserved | 
      <router-link to="/impressum" class="footer-link">Impressum</router-link> | 
      <router-link to="/dataprotection" class="footer-link">Datenschutz</router-link> 
      </div>
    </footer>
  </div>
</template>


<script>
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";

export default {
  name: "App",
  data() {
    return {
      isDarkMode: false, // Dark Mode Status
      user: null, // Aktueller Benutzerstatus
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      // Speichere den Dark Mode Status im Local Storage
      localStorage.setItem("isDarkMode", this.isDarkMode);
    },
    goToLogin() {
      this.$router.push("/login");
    },
    goToRegister() {
      this.$router.push("/register");
    },
    async logout() {
      const auth = getAuth();
      try {
        await signOut(auth);
        this.user = null;
        this.$router.push("/");
      } catch (error) {
        console.error("Logout failed:", error.message);
      }
    },
  },
  created() {
    // Lade den Dark Mode Status aus dem Local Storage
    const savedMode = localStorage.getItem("isDarkMode");
    if (savedMode !== null) {
      this.isDarkMode = JSON.parse(savedMode);
    }

    // Überprüfe den Authentifizierungsstatus
    const auth = getAuth();
    onAuthStateChanged(auth, (user) => {
      this.user = user;
    });
  },
};
</script>

<style scoped>
/* Grundlegende Stile für die App */

.footer-link {
  color: rgb(131, 10, 131);  /* This sets the text color to violet */
  text-decoration: none;  /* Optional: removes underline */
}

.footer-link:hover {
  text-decoration: underline;  /* Optional: adds underline on hover */
}

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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s, box-shadow 0.3s;
}

#app.dark-mode .top-navbar {
  background-color: #1e1e1e;
  box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
}

/* Navigation Links */
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

/* Auth Buttons */
.auth-button-group {
  display: flex;
  gap: 10px; /* Einheitlicher Abstand zwischen Buttons */
}

.auth-button {
  background-color: #20c997;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s, transform 0.2s;
}

.auth-button:hover {
  background-color: #1aa179;
}

.auth-button:active {
  transform: scale(0.98);
}

#app.dark-mode .auth-button {
  background-color: #bb86fc;
}

#app.dark-mode .auth-button:hover {
  background-color: #985eff;
}

/* Responsive Anpassungen */
@media (max-width: 900px) {
  .top-navbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .top-navbar nav {
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 10px;
  }

  .auth-button-group {
    justify-content: flex-start;
    margin-top: 10px;
  }
}

</style>
