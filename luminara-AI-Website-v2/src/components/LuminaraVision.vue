<template>
  <div class="ollama-chat-vision">
    <h2>Powered by Llama 3.2-Vision and Flask-API</h2>
    <h4>
      Multimodaler Chatbot für die Kommunikation mit Llama 3.2-Vision, einem
      KI-Modell für Bild- und Textanfragen.
    </h4>

    <!-- Dark Mode Toggle Button -->
    <button class="dark-mode-toggle" @click="toggleDarkMode">
      {{ isDarkMode ? "Light Mode" : "Dark Mode" }}
    </button>

    <!-- Dropdown zur Auswahl des KI-Modells -->
    <div class="model-selection" :class="{ 'dark-mode': isDarkMode }">
      <label for="model">Wähle ein KI-Modell:</label>
      <select v-model="selectedModel" id="model">
        <option value="llama3.2-vision">Llama 3.2-Vision</option>
        <!-- Weitere Modelle können hier hinzugefügt werden -->
      </select>
    </div>

    <!-- Anzeige der Nachrichten im Chat-Format -->
    <div class="chat-box">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.type, { 'dark-mode': isDarkMode }]"
      >
        <p v-if="message.type === 'user'">{{ message.text }}</p>
        <div
          v-else-if="message.type === 'ollama'"
          v-html="renderMarkdown(message.text)"
          class="markdown-content"
        ></div>
      </div>
    </div>

    <!-- Eingabefeld, Bild-Upload und Button -->
    <div class="input-area">
      <input
        v-model="userInput"
        placeholder="Frag Llama 3.2-Vision..."
        @keydown.enter="sendMessage"
        class="chat-input"
      />
      <input
        type="file"
        @change="handleImageUpload"
        accept="image/*"
        class="image-input"
        multiple
      />
      <button @click="sendMessage" class="send-button" :disabled="loading">
        <i class="fas fa-paper-plane"></i> Absenden
      </button>
    </div>

    <div v-if="loading" class="loading">Lädt...</div>
    <div v-if="error" class="error">
      <p>
        Es gab ein Problem bei der Kommunikation mit Llama 3.2-Vision:
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import MarkdownIt from "markdown-it";
import markdownItKatex from "markdown-it-katex";
import "katex/dist/katex.min.css";
import hljs from "highlight.js";
import "highlight.js/styles/github.css"; // Optional: Für Syntax-Highlighting

export default {
  data() {
    return {
      userInput: "",
      loading: false,
      error: "",
      messages: [], // Hier werden die Nachrichten (Benutzer + Llama) gespeichert
      selectedModel: "llama3.2-vision", // Standardmäßig ausgewähltes Modell
      isDarkMode: false, // Dark Mode Status
      imageFiles: [], // Hier werden die hochgeladenen Bilder gespeichert
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === "" && this.imageFiles.length === 0) {
        this.error = "Prompt und/oder Bild dürfen nicht leer sein!";
        return;
      }

      // Füge die Benutzernachricht der Nachrichtenliste hinzu
      this.messages.push({ type: "user", text: this.userInput });

      this.loading = true;
      this.error = "";

      // Bereite die Bilder vor
      let base64Images = [];
      if (this.imageFiles.length > 0) {
        try {
          base64Images = await Promise.all(
            this.imageFiles.map((file) => this.convertToBase64(file))
          );
        } catch (e) {
          this.error = "Fehler beim Konvertieren der Bilder.";
          this.loading = false;
          return;
        }
      }

      const payload = {
        model: this.selectedModel,
        prompt: this.userInput, // Direktes Feld für den Prompt
        images: base64Images, // Direktes Feld für die Bilder
      };

      try {
        // Anfrage an das Flask-Backend senden
        const response = await axios.post(
          "http://localhost:5000/ask_ollama_vision",
          payload
        );

        if (response.data.choices) {
          const botResponse = response.data.choices[0].text;
          this.messages.push({ type: "ollama", text: botResponse });
        } else if (response.data.error) {
          this.error = response.data.error;
        }
      } catch (err) {
        this.error = `Fehler: ${err.message}`;
      } finally {
        this.loading = false;
        this.userInput = ""; // Eingabefeld zurücksetzen
        this.imageFiles = []; // Zurücksetzen der Bild-Dateien
        this.$nextTick(() => {
          this.attachCopyButtons();
        });
      }
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.body.classList.toggle("dark-mode", this.isDarkMode);
      this.$el
        .querySelector(".ollama-chat-vision")
        .classList.toggle("dark-mode", this.isDarkMode);
    },
    renderMarkdown(text) {
      const md = new MarkdownIt({
        html: true,
        linkify: true,
        typographer: true,
        breaks: true,
        highlight: function (str, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return (
                '<pre class="hljs"><code>' +
                hljs.highlight(str, { language: lang, ignoreIllegals: true })
                  .value +
                "</code></pre>"
              );
            } catch (__) {
              /* Fehler ignorieren */
            }
          }

          return (
            '<pre class="hljs"><code>' +
            md.utils.escapeHtml(str) +
            "</code></pre>"
          );
        },
      }).use(markdownItKatex);

      // Überschreiben des Codeblock-Renderers
      md.renderer.rules.fence = function (tokens, idx) {
        // Prefix unused vars with _
        const token = tokens[idx];
        const code = token.content;
        const lang = token.info.trim().split(/\s+/g)[0];

        // Generiere eine eindeutige ID für den Codeblock
        const uniqueId = `copy-btn-${idx}-${Math.random()
          .toString(36)
          .substr(2, 9)}`;

        // Render den Codeblock mit einem Copy-Button
        return `
            <div class="code-block">
              <button class="copy-button" data-clipboard-target="#${uniqueId}">Copy</button>
              <pre class="hljs"><code id="${uniqueId}" class="${lang}">${md.utils.escapeHtml(
          code
        )}</code></pre>
            </div>
          `;
      };

      return md.render(text);
    },
    attachCopyButtons() {
      const buttons = this.$el.querySelectorAll(".copy-button");
      buttons.forEach((button) => {
        button.addEventListener("click", () => {
          const target = button.getAttribute("data-clipboard-target");
          const codeElement = this.$el.querySelector(target);
          if (codeElement) {
            const text = codeElement.innerText;
            navigator.clipboard
              .writeText(text)
              .then(() => {
                // Optional: Feedback für den Nutzer
                button.textContent = "Copied!";
                setTimeout(() => {
                  button.textContent = "Copy";
                }, 2000);
              })
              .catch((err) => {
                console.error("Kopieren fehlgeschlagen:", err);
              });
          }
        });
      });
    },
    handleImageUpload(event) {
      const files = event.target.files;
      if (files && files.length > 0) {
        this.imageFiles = Array.from(files).slice(0, 5); // Beschränke auf maximal 5 Bilder
      }
    },
    convertToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },
  },
  watch: {
    messages() {
      this.$nextTick(() => {
        const chatBox = this.$el.querySelector(".chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    },
  },
  mounted() {
    // Initiales Anhängen der Copy-Buttons falls es schon Nachrichten gibt
    this.$nextTick(() => {
      this.attachCopyButtons();
    });
  },
};
</script>

<style scoped>
/* Grundlegende Stile für die Chat-Komponente */
.ollama-chat-vision {
  font-family: "Roboto", sans-serif;
  margin: 20px auto;
  padding: 25px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 12px;
  max-width: 700px;
  background-color: #f0f4f8; /* Helles Grau für den allgemeinen Hintergrund */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative; /* Für den Dark Mode Toggle Button */
}

/* Dark Mode Stile */
.ollama-chat-vision.dark-mode {
  background-color: #1e1e1e; /* Dunkles Grau für den Hintergrund */
  border-color: #444; /* Dunkleres Grau für Ränder */
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1); /* Heller Schatten */
}

.ollama-chat-vision.dark-mode h2 {
  color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

/* Dark Mode Toggle Button */
.dark-mode-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #20c997; /* Lebendiges Türkis */
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dark-mode-toggle:hover {
  background-color: #1aa179; /* Etwas dunkleres Türkis für Hover */
}

.dark-mode-toggle:active {
  transform: scale(0.98);
}

.ollama-chat-vision.dark-mode .dark-mode-toggle {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

.ollama-chat-vision.dark-mode .dark-mode-toggle:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Überschrift */
.ollama-chat-vision h2 {
  font-size: 1.8rem;
  color: #1e90ff; /* Kräftiges Blau */
  text-align: center;
  margin-bottom: 10px;
}

/* Modell-Auswahl */
.model-selection {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.model-selection label {
  font-weight: 500;
  color: #333;
}

.ollama-chat-vision.dark-mode .model-selection label {
  color: #fff;
}

.model-selection select {
  padding: 10px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  transition: border-color 0.3s;
}

.ollama-chat-vision.dark-mode .model-selection select {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

.model-selection select:focus {
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
  outline: none;
}

.ollama-chat-vision.dark-mode .model-selection select:focus {
  border-color: #bb86fc; /* Kräftiges Lila für Fokus im Dark Mode */
}

/* Chat-Box */
.chat-box {
  flex: 1;
  max-height: 400px;
  overflow-y: auto;
  padding: 15px;
  background-color: #ffffff; /* Weiß für Chat-Bubbles */
  border-radius: 10px;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05); /* Leichter innerer Schatten */
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ollama-chat-vision.dark-mode .chat-box {
  background-color: #2a2f32; /* Dunkleres Grau für Chat-Bubbles im Dark Mode */
  box-shadow: inset 0 2px 8px rgba(255, 255, 255, 0.1); /* Hellerer innerer Schatten */
}

/* Nachrichten */
.message {
  padding: 12px 20px;
  border-radius: 20px;
  max-width: 75%;
  word-wrap: break-word;
  position: relative;
  transition: background-color 0.3s, transform 0.2s;
}

.message.user {
  align-self: flex-end;
  background-color: #cce5ff; /* Hellblau für Benutzernachrichten */
  color: #004085; /* Dunkles Blau für Text */
}

.ollama-chat-vision.dark-mode .message.user {
  background-color: #3333cc; /* Dunkles Blau für Benutzernachrichten im Dark Mode */
  color: #e0e0e0; /* Helles Grau für Text im Dark Mode */
}

.message.ollama {
  align-self: flex-start;
  background-color: #d4edda; /* Hellgrün für Ollama-Nachrichten */
  color: #155724; /* Dunkles Grün für Text */
}

.ollama-chat-vision.dark-mode .message.ollama {
  background-color: #228b22; /* Dunkles Grün für Ollama-Nachrichten im Dark Mode */
  color: #f1f1f1; /* Helles Grau für Text im Dark Mode */
}

/* Eingabebereich */
.input-area {
  display: flex;
  gap: 10px;
}

.chat-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* Leichter Schatten */
  background-color: #fff;
  color: #333;
}

.ollama-chat-vision.dark-mode .chat-input {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

.chat-input:focus {
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
  outline: none;
}

.ollama-chat-vision.dark-mode .chat-input:focus {
  border-color: #bb86fc; /* Kräftiges Lila für Fokus im Dark Mode */
}

/* Bild-Upload */
.image-input {
  padding: 12px 15px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  color: #333;
}

.ollama-chat-vision.dark-mode .image-input {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

/* Senden-Button */
.send-button {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #1e90ff; /* Kräftiges Blau */
  color: #fff;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
}

.send-button:hover {
  background-color: #1c86ee; /* Etwas dunkleres Blau für Hover */
  transform: translateY(-2px);
}

.send-button:active {
  transform: translateY(0);
}

.ollama-chat-vision.dark-mode .send-button {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

.ollama-chat-vision.dark-mode .send-button:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Lade- und Fehleranzeige */
.loading {
  text-align: center;
  font-weight: bold;
  color: #ffc107; /* Warmes Gelb für Ladeanzeigen */
}

.error {
  text-align: center;
  color: #dc3545; /* Auffälliges Rot für Fehler */
  font-weight: bold;
  background-color: #f8d7da; /* Helleres Rot für Fehlerhintergrund */
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #dc3545; /* Auffälliges Rot für Fehler */
}

.ollama-chat-vision.dark-mode .error {
  background-color: #721c24; /* Dunkleres Rot für Fehlerhintergrund im Dark Mode */
  color: #f8d7da; /* Helles Rot für Text im Dark Mode */
  border-color: #f5c6cb; /* Hellere Ränder für Fehler im Dark Mode */
}

/* Code-Block Container */
.code-block {
  position: relative;
}

/* Copy-Button */
.copy-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #1e90ff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.3s;
}

.copy-button:hover {
  background-color: #0d6efd;
}

.copy-button:active {
  background-color: #0a58ca;
}

/* Styling für Codeblöcke im Dark Mode */
.ollama-chat-vision.dark-mode .copy-button {
  background-color: #bb86fc;
}

.ollama-chat-vision.dark-mode .copy-button:hover {
  background-color: #985eff;
}

/* Markdown-Inhalte */
.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 20px;
  color: #1e90ff;
}

.markdown-content p {
  line-height: 1.6;
}

.markdown-content pre {
  background-color: #eee;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.markdown-content code {
  background-color: #eee;
  padding: 2px 4px;
  border-radius: 3px;
}

/* Responsive Anpassungen */
@media (max-width: 768px) {
  .ollama-chat-vision {
    padding: 20px;
  }

  .chat-box {
    max-height: 300px;
  }

  .send-button {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .ollama-chat-vision {
    padding: 15px;
  }

  .model-selection {
    flex-direction: column;
  }

  .send-button {
    padding: 8px 12px;
    font-size: 0.8rem;
  }

  .chat-input {
    padding: 10px 12px;
  }

  .image-input {
    padding: 10px 12px;
  }
}
</style>
