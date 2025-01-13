<template>
  <div class="auth-container">
    <h1>Registrieren</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Benutzername</label>
        <input type="text" id="username" v-model="username" placeholder="Benutzername" required />
      </div>
      <div class="form-group">
        <label for="email">E-Mail</label>
        <input type="email" id="email" v-model="email" placeholder="E-Mail" required />
      </div>
      <div class="form-group">
        <label for="password">Passwort</label>
        <input type="password" id="password" v-model="password" placeholder="Passwort" required />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? "Registrieren..." : "Registrieren" }}
      </button>
    </form>
    <button @click="handleGoogleRegister" class="google-login-button">
      Mit Google registrieren
    </button>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p>Bereits ein Konto? <router-link to="/login">Hier anmelden</router-link>.</p>
  </div>
</template>

<script>
import { getAuth, createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { getFirestore, doc, setDoc, serverTimestamp, getDoc } from "firebase/firestore";

//Debugging
import { setLogLevel } from "firebase/firestore";
setLogLevel("debug");


export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      successMessage: "",
      errorMessage: "",
      loading: false,
    };
  },
  methods: {
    async handleRegister() {
      this.loading = true;
      const auth = getAuth();
      const db = getFirestore();

      try {
        const userCredential = await createUserWithEmailAndPassword(auth, this.email, this.password);
        const user = userCredential.user;

        // Benutzerinformationen in Firestore speichern
        await setDoc(doc(db, "users", user.uid), {
          username: this.username,
          tokens: 100,
          role: "student",
          registrationDate: serverTimestamp(),
          lastLogin: serverTimestamp(),
        });

        this.successMessage = "Erfolgreich registriert! Du kannst dich jetzt anmelden.";
        this.errorMessage = "";
        this.username = "";
        this.email = "";
        this.password = "";
      } catch (error) {
        this.errorMessage = "Registrierung fehlgeschlagen: " + error.message;
        this.successMessage = "";
      } finally {
        this.loading = false;
      }
    },
    async handleGoogleRegister() {
      const auth = getAuth();
      const db = getFirestore();
      const provider = new GoogleAuthProvider();

      try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;

        // Benutzerinformationen in Firestore speichern
        const userRef = doc(db, "users", user.uid);
        const userDoc = await getDoc(userRef);

        // Wenn der Benutzer noch nicht existiert, füge ihn hinzu
        if (!userDoc.exists()) {
          await setDoc(userRef, {
            username: user.displayName || "Google Benutzer",
            tokens: 100,
            role: "student",
            registrationDate: serverTimestamp(),
            lastLogin: serverTimestamp(),
          });
        }

        this.successMessage = "Mit Google erfolgreich registriert!";
        this.errorMessage = "";
        this.$router.push("/account");
      } catch (error) {
        this.errorMessage = "Google Registrierung fehlgeschlagen: " + error.message;
        this.successMessage = "";
      }
    },
  },
};
</script>

<style scoped>
.google-login-button {
  margin-top: 20px;
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100%;
}

.google-login-button:hover {
  background-color: #357ae8;
}


  .auth-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    text-align: center;
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
    text-align: left;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    width: 100%;
  }
  
  button:hover {
    background-color: #2980b9;
  }
  
  button:disabled {
    background-color: #ddd;
    cursor: not-allowed;
  }
  
  .success {
    color: green;
    margin-top: 20px;
  }
  
  .error {
    color: red;
    margin-top: 20px;
  }
  </style>
  