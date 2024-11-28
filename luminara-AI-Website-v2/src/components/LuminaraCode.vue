<template>
    <div class="programming-bot">
      <h2>Programmierbot</h2>
      <h4>Stelle deine Programmierfragen und erhalte präzise Antworten mit Codebeispielen.</h4>
  
      <!-- Dark Mode Toggle Button -->
      <button class="dark-mode-toggle" @click="toggleDarkMode">
        {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
      </button>
  
      <!-- Modellauswahl und Task-Auswahl -->
      <div class="selection-area">
        <div class="select-group">
          <label for="model-select">Modell auswählen:</label>
          <select id="model-select" v-model="selectedModel" class="select-input">
            <option v-for="model in models" :key="model.value" :value="model.value">
              {{ model.name }}
            </option>
          </select>
        </div>
  
        <div class="select-group">
          <label for="task-select">Aufgabe auswählen:</label>
          <select id="task-select" v-model="selectedTask" class="select-input">
            <option v-for="task in tasks" :key="task.value" :value="task.value">
              {{ task.name }}
            </option>
          </select>
        </div>
      </div>
  
      <!-- Chat-Box -->
      <div class="chat-box">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.type, { 'dark-mode': isDarkMode }]"
        >
          <!-- Benutzer-Nachricht -->
          <p v-if="message.type === 'user'">{{ message.text }}</p>
  
          <!-- Bot-Nachricht -->
          <div v-else-if="message.type === 'bot'" v-html="renderMarkdown(message.text)" class="markdown-content"></div>
  
          <!-- Refine Button für letzte Benutzer-Nachricht -->
          <button
            v-if="message.type === 'user' && isLastUserMessage(index) && !message.isRefined"
            class="refine-button"
            @click="prepareRefine(index)"
          >
            Refine
          </button>
  
          <!-- Button zum Anzeigen der ursprünglichen Benutzeranfrage und Bot-Antwort -->
          <button
            v-if="message.isRefined && !message.showOriginal"
            class="view-original-button"
            @click="toggleOriginal(index)"
          >
            Ursprüngliche Nachricht und Antwort anzeigen
          </button>
  
          <!-- Anzeige der ursprünglichen Benutzeranfrage und Bot-Antwort -->
          <div v-if="message.isRefined && message.showOriginal" class="original-message">
            <p><strong>Ursprüngliche Nachricht:</strong></p>
            <p>{{ message.originalUserText }}</p>
            <p><strong>Ursprüngliche Antwort:</strong></p>
            <div v-html="renderMarkdown(message.originalBotText)" class="markdown-content"></div>
            <button class="hide-original-button" @click="toggleOriginal(index)">
              Ursprüngliche Nachricht und Antwort verbergen
            </button>
          </div>
        </div>
      </div>
  
      <!-- Eingabefeld und Button -->
      <div class="input-area">
        <textarea
          v-model="userInput"
          placeholder="Stelle eine Programmierfrage..."
          @keydown.enter.exact.prevent="sendMessage"
          class="chat-input"
          rows="3"
        ></textarea>
        <button @click="sendMessage" class="send-button" :disabled="loading">
          <i class="fas fa-paper-plane"></i> Absenden
        </button>
      </div>
  
      <!-- Lade- und Fehleranzeige -->
      <div v-if="loading" class="loading">Lädt...</div>
      <div v-if="error" class="error">
        <p>Es gab ein Problem beim Kommunizieren mit dem Programmierbot: {{ error }}</p>
      </div>
  
      <!-- Prompt-Engineering Modal -->
      <div v-if="showRefineModal" class="modal-overlay" @click.self="closeRefineModal">
        <div class="modal-content">
          <h3>Prompt bearbeiten</h3>
          <textarea
            v-model="refineInput"
            class="refine-input"
            rows="4"
          ></textarea>
          <div class="modal-actions">
            <button @click="sendRefinedMessage" class="modal-send-button" :disabled="loading">
              Absenden
            </button>
            <button @click="closeRefineModal" class="modal-close-button">Abbrechen</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  //FIXME: Copy Button funktioniert nicht wenn man refined!!!!

  import axios from "axios";
  import MarkdownIt from "markdown-it";
  import markdownItKatex from "markdown-it-katex";
  import "katex/dist/katex.min.css";
  import hljs from 'highlight.js';
  import 'highlight.js/styles/github.css'; // Optional: Für Syntax-Highlighting
  
  export default {
    data() {
      return {
        userInput: "",
        loading: false,
        error: "",
        messages: [], // Hier werden die Nachrichten (Benutzer + Bot) gespeichert
        isDarkMode: false, // Dark Mode Status
        models: [ // Liste der verfügbaren Modelle
          { name: "Qwen2.5-Coder 0.5B", value: "qwen2.5-coder:0.5b" },
          { name: "Qwen2.5-Coder 1.5B", value: "qwen2.5-coder:1.5b" },
          { name: "Qwen2.5-Coder 3B", value: "qwen2.5-coder:3b" },
          { name: "Qwen2.5-Coder 7B", value: "qwen2.5-coder" },

          { name: "CodeLlama", value: "codellama" },
          // Weitere Modelle können hier hinzugefügt werden
        ],
        selectedModel: "qwen2.5-coder:0.5b", // Standardmodell
        tasks: [ // Liste der verfügbaren Tasks mit zugehörigen System-Prompts
          { name: "Allgemeines Programmieren", value: "general" },
          { name: "Java Programmieren", value: "java" },
          { name: "Python Programmieren", value: "python" },
          { name: "ESP32 Programmieren", value: "esp32" },
          { name: "Raspberry Pi Programmieren", value: "raspberry_pi" },
          // Weitere Tasks können hier hinzugefügt werden
        ],
        selectedTask: "general", // Standardaufgabe
        systemPrompts: { // System-Prompts für die verschiedenen Tasks
          general: "Du bist ein hilfreicher Programmierbot, der präzise und verständliche Antworten mit Codebeispielen liefert.",
          java: "Du bist ein Experte in Java-Programmierung. Hilf mir mit klaren und effizienten Java-Codebeispielen.",
          python: "Du bist ein Experte in Python-Programmierung. Hilf mir mit klaren und effizienten Python-Codebeispielen.",
          esp32: "Du bist ein Experte in der Programmierung von ESP32 Mikrocontrollern. Hilf mir mit klaren und effizienten Codebeispielen für ESP32.",
          raspberry_pi: "Du bist ein Experte in der Programmierung von Raspberry Pi. Hilf mir mit klaren und effizienten Codebeispielen für Raspberry Pi.",
          // Weitere System-Prompts können hier hinzugefügt werden
        },
        showRefineModal: false, // Status für das Refine Modal
        refineIndex: null, // Index der Nachricht, die bearbeitet werden soll
        refineInput: "", // Eingabe für das Refine Modal
      };
    },
    methods: {
      async sendMessage() {
        if (this.userInput.trim() === "") {
          this.error = "Die Eingabe darf nicht leer sein!";
          return;
        }
  
        // Füge die Benutzernachricht der Nachrichtenliste hinzu
        this.messages.push({ type: "user", text: this.userInput });
  
        this.loading = true;
        this.error = "";
  
        // Bereite die System-Prompt basierend auf der ausgewählten Aufgabe vor
        const systemPrompt = this.systemPrompts[this.selectedTask] || this.systemPrompts['general'];
  
        const payload = {
          model: this.selectedModel, // Verwende das ausgewählte Modell
          prompt: `${systemPrompt}\n${this.userInput}`, // Kombiniere System-Prompt und Benutzer-Eingabe
        };
  
        try {
          // Anfrage an das Flask-Backend senden
          const response = await axios.post("http://localhost:5000/ask_programming_bot", payload);
          
          if (response.data.choices) {
            const botResponse = response.data.choices[0].text;
            this.messages.push({ type: "bot", text: botResponse });
          } else if (response.data.error) {
            this.error = response.data.error;
          }
        } catch (err) {
          this.error = `Fehler: ${err.message}`;
        } finally {
          this.loading = false;
          this.userInput = ""; // Eingabefeld zurücksetzen
          this.$nextTick(() => {
            this.attachCopyButtons();
          });
        }
      },
      toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        document.body.classList.toggle('dark-mode', this.isDarkMode);
        this.$el.querySelector('.programming-bot').classList.toggle('dark-mode', this.isDarkMode);
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
                return '<pre class="hljs"><code>' +
                       hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
                       '</code></pre>';
              } catch (__) { /* Fehler ignorieren */ }
            }
  
            return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
          }
        }).use(markdownItKatex);
  
        // Überschreiben des Codeblock-Renderers
        md.renderer.rules.fence = (tokens, idx) => {
          const token = tokens[idx];
          const code = token.content;
          const lang = token.info.trim().split(/\s+/g)[0];
  
          // Generiere eine eindeutige ID für den Codeblock
          const uniqueId = `copy-btn-${idx}-${Math.random().toString(36).substr(2, 9)}`;
  
          // Render den Codeblock mit einem Copy-Button
          return `
            <div class="code-block">
              <button class="copy-button" data-clipboard-target="#${uniqueId}">Copy</button>
              <pre class="hljs"><code id="${uniqueId}" class="${lang}">${md.utils.escapeHtml(code)}</code></pre>
            </div>
          `;
        };
  
        return md.render(text);
      },
      attachCopyButtons() {
        const buttons = this.$el.querySelectorAll('.copy-button');
        buttons.forEach(button => {
          button.addEventListener('click', () => {
            const target = button.getAttribute('data-clipboard-target');
            const codeElement = this.$el.querySelector(target);
            if (codeElement) {
              const text = codeElement.innerText;
              navigator.clipboard.writeText(text).then(() => {
                // Optional: Feedback für den Nutzer
                button.textContent = 'Copied!';
                setTimeout(() => {
                  button.textContent = 'Copy';
                }, 2000);
              }).catch(err => {
                console.error('Kopieren fehlgeschlagen:', err);
              });
            }
          });
        });
      },
      copyText(text) {
        navigator.clipboard.writeText(text).then(
          () => {
            alert("Text wurde in die Zwischenablage kopiert!");
          },
          () => {
            alert("Kopieren fehlgeschlagen!");
          }
        );
      },
      isLastUserMessage(index) {
        for (let i = this.messages.length - 1; i >= 0; i--) {
          if (this.messages[i].type === 'user') {
            return i === index;
          }
        }
        return false;
      },
      prepareRefine(index) {
        this.refineIndex = index;
        this.refineInput = this.messages[index].text;
        this.showRefineModal = true;
      },
      closeRefineModal() {
        this.showRefineModal = false;
        this.refineIndex = null;
        this.refineInput = "";
      },
      async sendRefinedMessage() {
        if (this.refineInput.trim() === "") {
          this.error = "Die Eingabe darf nicht leer sein!";
          return;
        }
  
        // Speichere die ursprüngliche Benutzer-Nachricht und Bot-Antwort
        const originalUserText = this.messages[this.refineIndex].text;
        const originalBotText = this.messages[this.refineIndex + 1]?.text || "";
  
        // Entferne die ursprüngliche Benutzer-Nachricht und Bot-Antwort
        this.messages.splice(this.refineIndex, 2);
  
        // Füge die verfeinerte Benutzer-Nachricht hinzu
        this.messages.push({ 
          type: "user", 
          text: this.refineInput,
          isRefined: true,
          originalUserText: originalUserText, // Speichert die ursprüngliche Benutzeranfrage
          originalBotText: originalBotText,   // Speichert die ursprüngliche Bot-Antwort
          showOriginal: false
        });
  
        this.loading = true;
        this.error = "";
        this.showRefineModal = false;
  
        // Bereite die System-Prompt basierend auf der ausgewählten Aufgabe vor
        const systemPrompt = this.systemPrompts[this.selectedTask] || this.systemPrompts['general'];
  
        const payload = {
          model: this.selectedModel, // Verwende das ausgewählte Modell
          prompt: `${systemPrompt}\n${this.refineInput}`, // Kombiniere System-Prompt und verfeinerten Benutzer-Eingabe
        };
  
        try {
          // Anfrage an das Flask-Backend senden
          const response = await axios.post("http://localhost:5000/ask_programming_bot", payload);
          
          if (response.data.choices) {
            const botResponse = response.data.choices[0].text;
            this.messages.push({ type: "bot", text: botResponse });
          } else if (response.data.error) {
            this.error = response.data.error;
          }
        } catch (err) {
          this.error = `Fehler: ${err.message}`;
        } finally {
          this.loading = false;
          this.$nextTick(() => {
            this.attachCopyButtons();
          });
        }
      },
      toggleOriginal(index) {
        const message = this.messages[index];
        if (message.isRefined) {
          message.showOriginal = !message.showOriginal;
          if (message.showOriginal) {
            // Füge die ursprüngliche Benutzer-Nachricht und Bot-Antwort ein
            const originalUserMessage = {
              type: "user",
              text: message.originalUserText,
              hidden: true
            };
            const originalBotMessage = {
              type: "bot",
              text: message.originalBotText,
              hidden: true
            };
            // Füge die ursprünglichen Nachrichten direkt nach der verfeinerten Nachricht ein
            this.messages.splice(index + 1, 0, originalUserMessage, originalBotMessage);
          } else {
            // Entferne die ursprünglichen Nachrichten
            this.messages.splice(index + 1, 2);
          }
        }
      },
    },
    watch: {
      messages() {
        this.$nextTick(() => {
          const chatBox = this.$el.querySelector('.chat-box');
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
  /* Grundlegende Stile für die Programmierbot-Komponente */
  .programming-bot {
    font-family: 'Roboto', sans-serif;
    margin: 20px auto;
    padding: 25px;
    border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
    border-radius: 12px;
    max-width: 900px; /* Größer für bessere Aufteilung */
    background-color: #f0f4f8; /* Helles Grau für den allgemeinen Hintergrund */
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
    display: flex;
    flex-direction: column;
    gap: 20px;
    position: relative; /* Für den Dark Mode Toggle Button */
  }
  
  /* Dark Mode Stile */
  .programming-bot.dark-mode {
    background-color: #1e1e1e; /* Dunkles Grau für den Hintergrund */
    border-color: #444; /* Dunkleres Grau für Ränder */
    box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1); /* Heller Schatten */
  }
  
  .programming-bot.dark-mode h2 {
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
  
  .programming-bot.dark-mode .dark-mode-toggle {
    background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
  }
  
  .programming-bot.dark-mode .dark-mode-toggle:hover {
    background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
  }
  
  /* Auswahlbereich */
  .selection-area {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .select-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex: 1;
  }
  
  .select-group label {
    font-weight: bold;
    color: #333;
  }
  
  .programming-bot.dark-mode .select-group label {
    color: #f8f9fa;
  }
  
  .select-input {
    padding: 8px 12px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 1rem;
    background-color: #fff;
    color: #333;
    transition: border-color 0.3s;
  }
  
  .programming-bot.dark-mode .select-input {
    background-color: #333;
    color: #fff;
    border-color: #1e90ff;
  }
  
  .select-input:focus {
    border-color: #1e90ff;
    outline: none;
  }
  
  .programming-bot.dark-mode .select-input:focus {
    border-color: #bb86fc;
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
  
  .programming-bot.dark-mode .chat-box {
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
  
  .programming-bot.dark-mode .message.user {
    background-color: #3333cc; /* Dunkles Blau für Benutzernachrichten im Dark Mode */
    color: #e0e0e0; /* Helles Grau für Text im Dark Mode */
  }
  
  .message.bot {
    align-self: flex-start;
    background-color: #d4edda; /* Hellgrün für Bot-Nachrichten */
    color: #155724; /* Dunkles Grün für Text */
  }
  
  .programming-bot.dark-mode .message.bot {
    background-color: #228B22; /* Dunkles Grün für Bot-Nachrichten im Dark Mode */
    color: #f1f1f1; /* Helles Grau für Text im Dark Mode */
  }
  
  /* Refine Button */
  .refine-button {
    margin-top: 5px;
    background-color: #ffc107; /* Gelb für Refine */
    color: #212529;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: background-color 0.3s;
  }
  
  .refine-button:hover {
    background-color: #e0a800;
  }
  
  .programming-bot.dark-mode .refine-button {
    background-color: #ff9800;
    color: #fff;
  }
  
  .programming-bot.dark-mode .refine-button:hover {
    background-color: #e68900;
  }
  
  /* View Original Button */
  .view-original-button {
    margin-top: 5px;
    background-color: #17a2b8; /* Blau für View Original */
    color: #fff;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: background-color 0.3s;
  }
  
  .view-original-button:hover {
    background-color: #138496;
  }
  
  .programming-bot.dark-mode .view-original-button {
    background-color: #17a2b8;
  }
  
  .programming-bot.dark-mode .view-original-button:hover {
    background-color: #117a8b;
  }
  
  /* Original Message Anzeige */
  .original-message {
    margin-top: 10px;
    padding: 10px;
    background-color: #f8d7da; /* Helles Rot für ursprüngliche Nachricht */
    color: #721c24; /* Dunkles Rot für Text */
    border-radius: 5px;
    position: relative;
  }
  
  .programming-bot.dark-mode .original-message {
    background-color: #721c24; /* Dunkleres Rot für ursprüngliche Nachricht im Dark Mode */
    color: #f8d7da; /* Helles Rot für Text im Dark Mode */
  }
  
  .hide-original-button {
    margin-top: 5px;
    background-color: #dc3545; /* Rot für Hide Original */
    color: #fff;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: background-color 0.3s;
  }
  
  .hide-original-button:hover {
    background-color: #c82333;
  }
  
  .programming-bot.dark-mode .hide-original-button {
    background-color: #dc3545;
  }
  
  .programming-bot.dark-mode .hide-original-button:hover {
    background-color: #bd2130;
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
    resize: none;
  }
  
  .programming-bot.dark-mode .chat-input {
    background-color: #333;
    color: #fff;
    border-color: #1e90ff; /* Kräftiges Blau für Fokus */
  }
  
  .chat-input:focus {
    border-color: #1e90ff; /* Kräftiges Blau für Fokus */
    outline: none;
  }
  
  .programming-bot.dark-mode .chat-input:focus {
    border-color: #bb86fc; /* Kräftiges Lila für Fokus im Dark Mode */
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
  
  .programming-bot.dark-mode .send-button {
    background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
  }
  
  .programming-bot.dark-mode .send-button:hover {
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
  
  .programming-bot.dark-mode .error {
    background-color: #721c24; /* Dunkleres Rot für Fehlerhintergrund im Dark Mode */
    color: #f8d7da; /* Helles Rot für Text im Dark Mode */
    border-color: #f5c6cb; /* Hellere Ränder für Fehler im Dark Mode */
  }
  
  /* Textabschnitte */
  .texts-container {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .text-section {
    flex: 1 1 45%; /* Zwei Spalten bei ausreichend Platz */
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .raw-text-section,
  .improved-text-section {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    position: relative;
  }
  
  .programming-bot.dark-mode .raw-text-section,
  .programming-bot.dark-mode .improved-text-section {
    background-color: #343a40;
    color: #f8f9fa;
  }
  
  .raw-text-section pre {
    white-space: pre-wrap; /* Zeilenumbrüche beibehalten */
    background-color: #e9ecef;
    padding: 10px;
    border-radius: 4px;
    overflow-x: auto;
  }
  
  .programming-bot.dark-mode .raw-text-section pre {
    background-color: #495057;
    color: #f8f9fa;
  }
  
  .improved-text-section div {
    /* Stil für das gerenderte Markdown */
  }
  
  .copy-button {
    align-self: flex-end;
    background-color: #28a745; /* Grün für Kopieren */
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s;
  }
  
  .copy-button:hover {
    background-color: #218838;
  }
  
  .copy-button:active {
    background-color: #1e7e34;
  }
  
  .programming-bot.dark-mode .copy-button {
    background-color: #28a745;
  }
  
  .programming-bot.dark-mode .copy-button:hover {
    background-color: #218838;
  }
  
  .programming-bot.dark-mode .copy-button:active {
    background-color: #1e7e34;
  }
  
  /* Verbesserter Text */
  .improved-text {
    background-color: #d4edda; /* Hellgrün für verbesserte Texte */
    padding: 15px;
    border-radius: 8px;
  }
  
  .programming-bot.dark-mode .improved-text {
    background-color: #228B22; /* Dunkles Grün für verbesserte Texte im Dark Mode */
    color: #f1f1f1; /* Helles Grau für Text im Dark Mode */
  }
  
  /* Code-Block Container */
  .code-block {
    position: relative;
  }
  
  /* Copy-Button für Code-Blöcke */
  .code-block .copy-button {
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
  
  .code-block .copy-button:hover {
    background-color: #0d6efd;
  }
  
  .code-block .copy-button:active {
    background-color: #0a58ca;
  }
  
  .programming-bot.dark-mode .code-block .copy-button {
    background-color: #bb86fc;
  }
  
  .programming-bot.dark-mode .code-block .copy-button:hover {
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
    .programming-bot {
      padding: 20px;
    }
  
    .chat-box {
      max-height: 300px;
    }
  
    .send-button {
      padding: 10px 16px;
      font-size: 0.9rem;
    }
  
    .selection-area {
      flex-direction: column;
    }
  
    .text-section {
      flex: 1 1 100%;
    }
  }
  
  @media (max-width: 480px) {
    .programming-bot {
      padding: 15px;
    }
  
    .send-button {
      padding: 8px 12px;
      font-size: 0.8rem;
    }
  
    .chat-input {
      padding: 10px 12px;
    }
  }
  
  /* Modal-Stile */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .programming-bot.dark-mode .modal-content {
    background-color: #2a2f32;
    color: #f8f9fa;
  }
  
  .refine-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    font-size: 1rem;
    resize: vertical;
    background-color: #fff;
    color: #333;
  }
  
  .programming-bot.dark-mode .refine-input {
    background-color: #333;
    color: #fff;
    border-color: #1e90ff;
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 10px;
  }
  
  .modal-send-button {
    background-color: #1e90ff;
    color: #fff;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .modal-send-button:hover {
    background-color: #1c86ee;
  }
  
  .modal-send-button:active {
    background-color: #0a58ca;
  }
  
  .modal-close-button {
    background-color: #6c757d;
    color: #fff;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .modal-close-button:hover {
    background-color: #5a6268;
  }
  
  .programming-bot.dark-mode .modal-send-button {
    background-color: #bb86fc;
  }
  
  .programming-bot.dark-mode .modal-send-button:hover {
    background-color: #985eff;
  }
  
  .programming-bot.dark-mode .modal-close-button {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .programming-bot.dark-mode .modal-close-button:hover {
    background-color: #f5c6cb;
  }
  
  /* Original Message Anzeige */
  .original-message {
    margin-top: 10px;
    padding: 10px;
    background-color: #f8d7da; /* Helles Rot für ursprüngliche Nachricht */
    color: #721c24; /* Dunkles Rot für Text */
    border-radius: 5px;
    position: relative;
  }
  
  .programming-bot.dark-mode .original-message {
    background-color: #721c24; /* Dunkleres Rot für ursprüngliche Nachricht im Dark Mode */
    color: #f8d7da; /* Helles Rot für Text im Dark Mode */
  }
  
  .hide-original-button {
    margin-top: 5px;
    background-color: #dc3545; /* Rot für Hide Original */
    color: #fff;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: background-color 0.3s;
  }
  
  .hide-original-button:hover {
    background-color: #c82333;
  }
  
  .programming-bot.dark-mode .hide-original-button {
    background-color: #dc3545;
  }
  
  .programming-bot.dark-mode .hide-original-button:hover {
    background-color: #bd2130;
  }
  </style>
  