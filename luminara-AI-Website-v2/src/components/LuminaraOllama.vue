<template>
  <div class="chat-container">
    <!-- Haupt-Chatbereich -->
    <main class="chat-window">
      <h2>Powered by Ollama and Flask-API</h2>
      <h4>Kommunikation mit Ollama (LLaMA-Modell)</h4>

      <!-- Dropdown zur Auswahl des KI-Modells -->
      <div class="model-selection">
        <label for="model">Wähle ein KI-Modell:</label>
        <select v-model="selectedModel" id="model">
          <option value="llama3.2:1b">LLaMA 3.2 - 1B (schnell)</option>
          <option value="llama3.2">LLaMA 3.2 - 2B (neuestes Modell)</option>
          <option value="gemma2:27b">Gemma2:27b von Google</option>
          <option value="llava:13b">LLaVA 13B (langsam)</option>
          <option value="phi4">Neuestes Modell von Microsoft</option>
          <option value="deepseek-r1">DeepSeek R1 With Thinking capailities</option>
        </select>
      </div>

      <h3 v-if="currentChat">{{ currentChat.name }}</h3>
      <p v-else class="no-chat">Bitte wähle einen Chat oder starte einen neuen.</p>

      <div class="chat-box" v-if="currentChat">
        <div
          v-for="(message, index) in currentChat.messages"
          :key="index"
          :class="['message', message.type]"
        >
          <p v-if="message.type === 'user'">{{ message.text }}</p>
          <div
            v-else-if="message.type === 'ollama'"
            v-html="renderMarkdown(message.text)"
            class="markdown-content"
          ></div>
        </div>
      </div>

      <div class="input-area" v-if="currentChat">
        <input
          v-model="userInput"
          placeholder="Frag Ollama..."
          @keydown.enter="sendMessage"
          class="chat-input"
        />
        <button @click="sendMessage" class="send-button" :disabled="loading">Absenden</button>
      </div>

      <div v-if="loading" class="loading">Lädt...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </main>

    <!-- Seitenleiste (positionierbar links oder rechts) -->
    <aside class="chat-sidebar">
      <h3>Gespeicherte Chats</h3>
      <ul class="chat-list">
        <li v-for="(chat, index) in chats" :key="index" class="chat-item">
          <div class="chat-info">
            <strong @click="loadChat(chat.id)" :class="{ active: currentChat?.id === chat.id }">
              {{ chat.name }}
            </strong>
            <button @click.stop="deleteChat(chat.id)" class="delete-button" title="Chat löschen">🗑️</button>
          </div>
        </li>
      </ul>
      <button @click="startNewChat" class="new-chat-button">+ Neuer Chat</button>
    </aside>
  </div>
</template>


<script>
import axios from "axios";
import MarkdownIt from "markdown-it";
import markdownItKatex from "markdown-it-katex";
import "katex/dist/katex.min.css";

export default {
  data() {
    return {
      userInput: "",
      loading: false,
      error: "",
      chats: [], // Liste aller gespeicherten Chats
      currentChat: null, // Aktueller Chat
      selectedModel: "llama3.2:1b", // Ausgewähltes Modell
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === "") {
        this.error = "Prompt darf nicht leer sein!";
        return;
      }

      this.currentChat.messages.push({ type: "user", text: this.userInput });
      this.loading = true;
      this.error = "";

      try {
        const response = await axios.post("http://100.64.20.101:5000/ask_ollama", {
          prompt: this.userInput,
          model: this.selectedModel,
        });

        if (response.data.choices) {
          const botResponse = response.data.choices[0].text;
          this.currentChat.messages.push({ type: "ollama", text: botResponse });
          this.saveChat(); // Speichere den aktuellen Chat
        } else if (response.data.error) {
          this.error = response.data.error;
        }
      } catch (err) {
        this.error = `Fehler: ${err.message}`;
      } finally {
        this.loading = false;
        this.userInput = "";
      }
    },
    async loadChatList() {
      const savedChats = localStorage.getItem("ollama-chats");
      this.chats = savedChats ? JSON.parse(savedChats) : [];
    },
    async loadChat(chatId) {
      const chat = this.chats.find((chat) => chat.id === chatId);
      if (chat) {
        this.currentChat = chat;
      }
    },
    startNewChat() {
      const chatName = prompt("Bitte einen Namen für den neuen Chat eingeben:");
      if (!chatName) return;

      const newChat = {
        id: Date.now().toString(),
        name: chatName,
        messages: [],
      };

      this.chats.push(newChat);
      this.currentChat = newChat;
      this.saveChatList();
    },
    deleteChat(chatId) {
      if (!confirm("Möchtest du diesen Chat wirklich löschen?")) return;

      this.chats = this.chats.filter((chat) => chat.id !== chatId);
      if (this.currentChat?.id === chatId) {
        this.currentChat = null;
      }
      this.saveChatList();
    },
    saveChatList() {
      localStorage.setItem("ollama-chats", JSON.stringify(this.chats));
    },
    saveChat() {
      this.saveChatList();
    },
    renderMarkdown(text) {
      const md = new MarkdownIt().use(markdownItKatex);
      return md.render(text);
    },
  },
  mounted() {
    this.loadChatList();
  },
};
</script>
<style scoped>
/* Allgemeines Layout */
.chat-container {
  display: flex;
  height: 90vh;
  max-width: 1200px;
  margin: auto;
  background-color: #fdfdfd;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Haupt-Chatbereich */
.chat-window {
  flex: 3;
  padding: 30px;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
}

h3 {
  font-size: 1.8rem;
  font-weight: bold;
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.chat-header {
  background-color: #007bff;
  padding: 15px 20px;
  border-radius: 12px;
  color: white;
  text-align: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.chat-header:hover {
  transform: scale(1.02);
}

.model-selection {
  margin-bottom: 15px;
}

.model-selection label {
  font-weight: bold;
  margin-right: 8px;
}

.model-selection select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ced4da;
}

.no-chat {
  color: #666;
  font-size: 1.2rem;
}

.chat-box {
  flex: 1;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.message {
  padding: 12px 20px;
  border-radius: 16px;
  max-width: 70%;
  margin-bottom: 10px;
  line-height: 1.6;
}

.message.user {
  align-self: flex-end;
  background-color: #d8e8ff;
  color: #003f7f;
}

.message.ollama {
  align-self: flex-start;
  background-color: #e7f5e7;
  color: #225c22;
}

.markdown-content {
  white-space: pre-wrap;
  word-break: break-word;
}

/* Sidebar */
.chat-sidebar {
  flex: 1;
  background-color: #eef1f5;
  padding: 20px;
  border-left: 1px solid #ddd;
  overflow-y: auto;
}

.chat-sidebar h3 {
  margin-bottom: 20px;
  font-size: 1.4rem;
}

.chat-list {
  list-style-type: none;
  padding: 0;
}

.chat-item {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
  transition: background-color 0.3s ease-in-out;
}

.chat-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-info strong {
  cursor: pointer;
  font-size: 1.1rem;
  color: #007acc;
  transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

.chat-info strong.active {
  font-weight: bold;
  background-color: rgba(0, 123, 255, 0.2);
  padding: 8px;
  border-radius: 8px;
  color: #0056b3;
}

.chat-info strong:hover {
  text-decoration: underline;
}

.delete-button {
  background: none;
  border: none;
  color: red;
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.delete-button:hover {
  transform: scale(1.1);
}

.new-chat-button {
  display: block;
  width: 100%;
  margin-top: 20px;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  text-align: center;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.new-chat-button:hover {
  background-color: #0056b3;
}

.input-area {
  display: flex;
  gap: 12px;
  margin-top: 15px;
}

.chat-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
}

.chat-input:focus {
  outline: none;
  border-color: #007bff;
}

.send-button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #0056b3;
}

.send-button:disabled {
  background-color: #999;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  font-weight: bold;
  color: #ffc107;
  margin-top: 10px;
}

.error {
  text-align: center;
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .chat-container {
    flex-direction: column-reverse;
  }

  .chat-sidebar {
    width: 100%;
  }

  .chat-window {
    padding: 20px 10px;
  }
}
</style>
