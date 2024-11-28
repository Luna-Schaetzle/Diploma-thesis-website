<template>
  <div class="account-dashboard">
    <!-- Header-Bereich -->
    <header class="header">
      <h1>Willkommen, {{ username || "Benutzer" }}</h1>
      <p class="role">Rolle: <span>{{ role }}</span></p>
    </header>

    <div class="content">
      <!-- Account-Informationen -->
      <section class="account-section">
        <h2>Deine Kontoinformationen</h2>
        <div class="info-grid">
          <div class="info-item">
            <strong>E-Mail:</strong>
            <p>{{ email }}</p>
          </div>
          <div class="info-item">
            <strong>Verbleibende Tokens:</strong>
            <p>{{ tokensDisplay }}</p>
          </div>
          <div class="info-item">
            <strong>Registriert am:</strong>
            <p>{{ formattedRegistrationDate }}</p>
          </div>
          <div class="info-item">
            <strong>Letztes Login:</strong>
            <p>{{ formattedLastLogin }}</p>
          </div>
        </div>
        <div class="account-actions">
          <button @click="resetPassword">Passwort zurücksetzen</button>
          <button v-if="role === 'student'" @click="requestStudentPlus">
            Student+ beantragen
          </button>
          <router-link v-if="role === 'admin'" to="/admin">
            <button class="admin-button">
              Admin Dashboard
            </button>
          </router-link>
          <button class="logout" @click="logout">Abmelden</button>
        </div>
      </section>

      <!-- Dashboard-Bereich (nur für Admins anzeigen) -->
      <section v-if="role === 'admin'" class="admin-dashboard-section">
        <h2>Admin Funktionen</h2>
        <div class="admin-actions">
          <router-link to="/admin">
            <button class="admin-button">
              Admin Dashboard
            </button>
          </router-link>
          <button @click="resetTokensTo100">Tokens auf 100 zurücksetzen</button>
          <!-- Weitere Admin-spezifische Aktionen hier hinzufügen -->
        </div>
      </section>

      <!-- User-spezifische Dashboard-Bereich -->
      <section class="dashboard-section" v-if="role !== 'admin'">
        <h2>Dashboard</h2>
        <div class="dashboard-widgets">
          <div class="widget">
            <h3>Verwendete Tokens</h3>
            <p>{{ usedTokensThisMonth }}</p>
          </div>
          <div class="widget">
            <h3>Funktionen</h3>
            <ul>
              <li><router-link to="/applications/ollama">Ollama KI</router-link></li>
              <li><router-link to="/applications/chat">Chat</router-link></li>
              <li><router-link to="/applications/image">Bilderkennung</router-link></li>
            </ul>
          </div>
        </div>
      </section>
    </div>

    <!-- Erfolg- und Fehlermeldungen -->
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { getAuth, sendPasswordResetEmail, signOut } from "firebase/auth";
import { getFirestore, doc, getDoc, updateDoc } from "firebase/firestore";

export default {
  data() {
    return {
      email: "",
      tokens: 0,
      username: "",
      role: "",
      registrationDate: null,
      lastLogin: null,
      usedTokensThisMonth: 0,
      successMessage: "",
      errorMessage: "",
    };
  },
  computed: {
    formattedRegistrationDate() {
      return this.registrationDate
        ? new Intl.DateTimeFormat("de-DE", {
            year: "numeric",
            month: "long",
            day: "numeric",
          }).format(this.registrationDate.toDate())
        : "Unbekannt";
    },
    formattedLastLogin() {
      return this.lastLogin
        ? new Intl.DateTimeFormat("de-DE", {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
          }).format(this.lastLogin.toDate())
        : "Unbekannt";
    },
    tokensDisplay() {
      return this.tokens;
    }
  },
  async created() {
    try {
      const auth = getAuth();
      const db = getFirestore();
      const currentUser = auth.currentUser;

      if (currentUser) {
        this.email = currentUser.email;

        const userRef = doc(db, "users", currentUser.uid);
        const userDoc = await getDoc(userRef); // Verwenden Sie getDoc statt userRef.get()
        if (userDoc.exists()) {
          const data = userDoc.data();
          this.tokens = data.tokens || 0;
          this.username = data.username || "";
          this.role = data.role || "student";
          this.registrationDate = data.registrationDate || null;
          this.lastLogin = data.lastLogin || null;
          this.usedTokensThisMonth = data.usedTokensThisMonth || 0;
        } else {
          this.errorMessage = "Benutzerdaten nicht gefunden.";
        }
      } else {
        this.errorMessage = "Benutzer ist nicht eingeloggt.";
        this.$router.push("/login");
      }
    } catch (err) {
      this.errorMessage = "Fehler beim Laden der Benutzerdaten: " + err.message;
    }
  },
  methods: {
    async resetPassword() {
      const auth = getAuth();
      try {
        await sendPasswordResetEmail(auth, this.email);
        this.successMessage = "Passwort-Zurücksetzen-E-Mail wurde gesendet.";
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage = "Fehler beim Zurücksetzen des Passworts: " + error.message;
        this.successMessage = "";
      }
    },
    async requestStudentPlus() {
      const db = getFirestore();
      const auth = getAuth();
      const currentUser = auth.currentUser;

      if (currentUser) {
        try {
          const userRef = doc(db, "users", currentUser.uid);
          await updateDoc(userRef, {
            studentPlusRequest: true,
          });
          this.successMessage = "Student+ Beantragung erfolgreich gesendet.";
          this.errorMessage = "";
        } catch (error) {
          this.errorMessage = "Fehler beim Beantragen von Student+: " + error.message;
          this.successMessage = "";
        }
      }
    },
    async logout() {
      const auth = getAuth();
      try {
        await signOut(auth);
        this.$router.push("/login");
      } catch (error) {
        this.errorMessage = "Fehler beim Abmelden: " + error.message;
        this.successMessage = "";
      }
    },
    async resetTokensTo100() {
      const db = getFirestore();
      const auth = getAuth();
      const currentUser = auth.currentUser;

      if (currentUser) {
        try {
          const userRef = doc(db, "users", currentUser.uid);
          await updateDoc(userRef, {
            tokens: 100,
          });
          this.successMessage = "Deine Tokens wurden auf 100 zurückgesetzt.";
          this.errorMessage = "";
        } catch (error) {
          this.errorMessage = "Fehler beim Zurücksetzen der Tokens: " + error.message;
          this.successMessage = "";
        }
      }
    },
  },
};
</script>

<style scoped>
.account-dashboard {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px;
  background: linear-gradient(to bottom, #ffffff, #f4f4f4);
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  font-family: Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin: 0;
}

.header .role span {
  font-weight: bold;
  color: #3498db;
}

.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.account-section,
.dashboard-section,
.admin-dashboard-section {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.account-section h2,
.dashboard-section h2,
.admin-dashboard-section h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.info-item {
  padding: 10px;
  background: #f9f9f9;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.account-actions button,
.admin-actions button {
  margin: 10px 5px;
  padding: 10px 20px;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.account-actions button:hover,
.admin-actions button:hover {
  background: #2980b9;
}

button.logout {
  background: #e74c3c;
}

button.logout:hover {
  background: #c0392b;
}

button.admin-button {
  background: #2ecc71;
}

button.admin-button:hover {
  background: #27ae60;
}

.dashboard-widgets {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.widget {
  padding: 20px;
  background: #f0f8ff;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.success {
  color: green;
  text-align: center;
  margin-top: 20px;
}

.error {
  color: red;
  text-align: center;
  margin-top: 20px;
}

/* Responsive Anpassungen */
@media (max-width: 768px) {
  .content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .account-dashboard {
    padding: 20px;
  }
}
</style>
