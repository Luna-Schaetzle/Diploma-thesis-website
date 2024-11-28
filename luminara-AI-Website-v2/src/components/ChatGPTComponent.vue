<template>
  <div class="chat-container">
    <h1>ChatGPT</h1>
    <div class="token-info">
      <p>Verbleibende Tokens: <strong>{{ tokens }}</strong></p>
    </div>

    <div class="model-selection">
      <label for="model">Wähle ein Modell:</label>
      <select v-model="selectedModel" id="model">
        <option value="gpt-4o">GPT-4o</option>  
        <option value="gpt-4o-mini">GPT-4 Mini</option>
      </select>
    </div>

    <div class="chat-box">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.type]"
      >
        <p>{{ message.text }}</p>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="userInput"
        placeholder="Schreibe etwas..."
        @keydown.enter="sendMessage"
        class="chat-input"
      />
      <button @click="sendMessage" :disabled="loading || tokens <= 0" class="send-button">
        Absenden
      </button>
    </div>

    <div v-if="loading" class="loading">Nachricht wird gesendet...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import OpenAI from "openai";
import { OPENAI_API_KEY } from "../secrets";
import { getAuth } from "firebase/auth";
import { getFirestore, doc, getDoc, setDoc, updateDoc } from "firebase/firestore";

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY,
  dangerouslyAllowBrowser:  true,
});

export default {
  data() {
    return {
      userInput: "",
      messages: [], // Aktueller Chatverlauf
      tokens: 0, // Verfügbare Tokens
      selectedModel: "gpt-4", // Standardmodell
      loading: false,
      error: "",
    };
  },
  async created() {
    try {
      const auth = getAuth();
      const db = getFirestore();

      const currentUser = auth.currentUser;

      if (currentUser) {
        const userDoc = await getDoc(doc(db, "users", currentUser.uid));
        if (userDoc.exists()) {
          this.tokens = userDoc.data().tokens; // Tokens laden
          this.loadChatHistory(currentUser.uid); // Chatverlauf laden
        } else {
          this.error = "Benutzerdaten nicht gefunden.";
        }
      } else {
        this.error = "Benutzer ist nicht eingeloggt.";
      }
    } catch (err) {
      this.error = "Fehler beim Laden der Daten: " + err.message;
    }
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === "") {
        this.error = "Eingabe darf nicht leer sein!";
        return;
      }

      if (this.tokens <= 0) {
        this.error = "Keine Tokens mehr verfügbar!";
        return;
      }

      this.messages.push({ type: "user", text: this.userInput }); // Nachricht hinzufügen
      this.loading = true;
      this.error = "";

      try {
        const auth = getAuth();
        const db = getFirestore();
        const currentUser = auth.currentUser;

        if (currentUser) {
          const userRef = doc(db, "users", currentUser.uid);
          const userDoc = await getDoc(userRef);

          if (userDoc.exists()) {
            const currentTokens = userDoc.data().tokens;

            if (currentTokens > 0) {
              // ChatGPT Anfrage
              const completion = await openai.chat.completions.create({
                model: this.selectedModel,
                messages: [
                  ...this.messages.map((msg) => ({
                    role: msg.type === "user" ? "user" : "assistant",
                    content: msg.text,
                  })),
                  { role: "user", content: this.userInput },
                ],
              });

              const botResponse = completion.choices[0].message.content;
              this.messages.push({ type: "bot", text: botResponse });

              // Token reduzieren und in der Datenbank aktualisieren
              await updateDoc(userRef, {
                tokens: currentTokens - 1,
              });

              this.tokens = currentTokens - 1; // Lokale Anzeige aktualisieren

              // Chatverlauf speichern
              await setDoc(doc(db, "users", currentUser.uid, "chats", "latest"), {
                messages: this.messages,
              });
            } else {
              this.error = "Nicht genug Tokens!";
            }
          } else {
            this.error = "Benutzer nicht gefunden.";
          }
        } else {
          this.error = "Benutzer ist nicht eingeloggt.";
        }
      } catch (err) {
        this.error = "Fehler bei der Anfrage: " + err.message;
      } finally {
        this.loading = false;
        this.userInput = ""; // Eingabe zurücksetzen
      }
    },
    async loadChatHistory(userId) {
      try {
        const db = getFirestore();
        const chatDoc = await getDoc(doc(db, "users", userId, "chats", "latest"));

        if (chatDoc.exists()) {
          this.messages = chatDoc.data().messages || [];
        }
      } catch (err) {
        console.error("Fehler beim Laden des Chatverlaufs:", err.message);
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  font-family: Arial, sans-serif;
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.token-info {
  margin-bottom: 15px;
  font-size: 16px;
}

.model-selection {
  margin-bottom: 15px;
}

.chat-box {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 15px;
  padding: 15px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.message.user {
  background-color: #cce5ff;
  align-self: flex-end;
}

.message.bot {
  background-color: #d4edda;
}

.input-area {
  display: flex;
  gap: 10px;
}

.chat-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.send-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.send-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading {
  color: #ffc107;
}

.error {
  color: red;
}
</style>
