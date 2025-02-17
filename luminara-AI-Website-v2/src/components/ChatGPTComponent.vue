<template>
  <div class="app-container">
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

      <!-- Chat-Auswahl -->
      <div class="chat-selection">
        <h3>Gespeicherte Chats</h3>
        <ul>
          <li v-for="(chat, index) in chats" :key="index" class="chat-item">
            <div class="chat-info">
              <strong @click="loadChat(chat.id)" class="chat-name">{{ chat.name }}</strong>
              <span @click.stop="deleteChat(chat.id)" class="delete-button">🗑️</span>
            </div>
            <p>{{ chat.messages.length }} Nachrichten</p>
          </li>
        </ul>
        <button @click="startNewChat" class="new-chat-button">Neuen Chat starten</button>
      </div>

      <!-- Aktueller Chat -->
      <div class="chat-box" v-if="currentChat">
        <h3>{{ currentChat.name }}</h3>
        <div v-for="(message, index) in currentChat.messages" :key="index" :class="['message', message.type]">
          <p>{{ message.text }}</p>
        </div>
      </div>

      <div class="input-area" v-if="currentChat">
        <input v-model="userInput" placeholder="Schreibe etwas..." @keydown.enter="sendMessage" class="chat-input" />
        <button @click="sendMessage" :disabled="loading || tokens <= 0" class="send-button">
          Absenden
        </button>
      </div>

      <div v-if="loading" class="loading">Nachricht wird gesendet...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
    <!-- Datenschutzhinweis -->
    <div class="privacy-notice">
      <h2>Datenschutzhinweis</h2>
      <p>
        Bei der Nutzung dieses Chatbots werden Ihre Eingaben an die
        ChatGPT-API von OpenAI übermittelt, um Antworten zu generieren. Bitte
        geben Sie keine persönlichen oder sensiblen Daten wie Namen,
        Adressen, E-Mail-Adressen oder finanzielle Informationen ein.
      </p>
      <p>
        Tipps zur Datensicherheit:
      <ul>
        <li>
          Vermeiden Sie die Eingabe von personenbezogenen Daten oder
          vertraulichen Informationen.
        </li>
        <li>
          Nutzen Sie den Chatbot ausschließlich für allgemeine Anfragen und
          vermeiden Sie die Preisgabe sensibler Details.
        </li>
        <li>
          Seien Sie sich bewusst, dass Ihre Eingaben zur Verbesserung der
          KI-Modelle verwendet werden könnten. Weitere Informationen finden
          Sie in der
          <a href="https://openai.com/policies/privacy-policy" target="_blank">Datenschutzerklärung von OpenAI</a>.
        </li>
      </ul>
      </p>
    </div>
  </div>
</template>

<script>
import OpenAI from "openai";
import { OPENAI_API_KEY } from "../secrets";
import { getAuth } from "firebase/auth";
import { getFirestore, collection, doc, getDoc, deleteDoc, getDocs, updateDoc, addDoc } from "firebase/firestore";

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY,
  dangerouslyAllowBrowser: true,
});

export default {
  data() {
    return {
      userInput: "",
      chats: [], // Liste der Chats
      currentChat: null, // Aktuell geladener Chat
      tokens: 0,
      selectedModel: "gpt-4o",
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
          this.loadChatList(currentUser.uid); // Liste der Chats laden
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
    async loadChatList(userId) {
      const db = getFirestore();
      const chatsRef = collection(db, "users", userId, "chats");
      const chatDocs = await getDocs(chatsRef);
      this.chats = chatDocs.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
    },
    async loadChat(chatId) {
      const db = getFirestore();
      const auth = getAuth();
      const currentUser = auth.currentUser;

      const chatDoc = await getDoc(doc(db, "users", currentUser.uid, "chats", chatId));
      if (chatDoc.exists()) {
        this.currentChat = { id: chatId, ...chatDoc.data() };
      }
    },
    async startNewChat() {
      const chatName = prompt("Bitte einen Namen für den neuen Chat eingeben:");
      if (!chatName) return;

      const db = getFirestore();
      const auth = getAuth();
      const currentUser = auth.currentUser;

      const newChatRef = await addDoc(collection(db, "users", currentUser.uid, "chats"), {
        name: chatName,
        messages: [],
      });

      this.chats.push({ id: newChatRef.id, name: chatName, messages: [] });
      this.currentChat = { id: newChatRef.id, name: chatName, messages: [] };
    },
    async sendMessage() {
      if (this.userInput.trim() === "") {
        this.error = "Eingabe darf nicht leer sein!";
        return;
      }

      if (this.tokens <= 0) {
        this.error = "Keine Tokens mehr verfügbar!";
        return;
      }

      this.currentChat.messages.push({ type: "user", text: this.userInput });
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
              const completion = await openai.chat.completions.create({
                model: this.selectedModel,
                messages: this.currentChat.messages.map((msg) => ({
                  role: msg.type === "user" ? "user" : "assistant",
                  content: msg.text,
                })),
              });

              const botResponse = completion.choices[0].message.content;
              this.currentChat.messages.push({ type: "bot", text: botResponse });

              await updateDoc(userRef, {
                tokens: currentTokens - 1,
              });

              this.tokens = currentTokens - 1;

              await updateDoc(doc(db, "users", currentUser.uid, "chats", this.currentChat.id), {
                name: this.currentChat.name,
                messages: this.currentChat.messages,
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
        this.userInput = "";
      }
    },
    async deleteChat(chatId) {
      if (!confirm("Möchtest du diesen Chat wirklich löschen?")) return;

      const db = getFirestore();
      const auth = getAuth();
      const currentUser = auth.currentUser;

      try {
        await deleteDoc(doc(db, "users", currentUser.uid, "chats", chatId));
        this.chats = this.chats.filter((chat) => chat.id !== chatId);

        if (this.currentChat?.id === chatId) {
          this.currentChat = null; // Wenn der gelöschte Chat der aktuelle war, diesen zurücksetzen
        }
      } catch (err) {
        this.error = "Fehler beim Löschen des Chats: " + err.message;
      }
    },
  },
};
</script>

<style scoped>

.app-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.chat-container {
  flex: 1;
  margin-right: 20px;
  /* Weitere bestehende Stile */
}

.privacy-notice {
  width: 300px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  /* Weitere bestehende Stile */
}

.privacy-notice h2 {
  margin-top: 0;
}

.privacy-notice ul {
  list-style-type: disc;
  margin-left: 20px;
}

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

.chat-selection {
  margin-bottom: 15px;
}

.chat-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-name {
  cursor: pointer;
}

.chat-name:hover {
  text-decoration: underline;
}

.delete-button {
  cursor: pointer;
  color: red;
}

.chat-item {
  padding: 5px;
  background-color: #f0f0f0;
  border-radius: 4px;
  margin-bottom: 5px;
}

.new-chat-button {
  margin-top: 10px;
}
</style>
