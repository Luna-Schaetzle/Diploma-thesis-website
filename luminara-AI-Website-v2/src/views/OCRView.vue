<template>
  <div class="ocr-component">
    <h2>OCR-Funktionalität</h2>
    <h4>Lade ein Bild hoch, um den Text zu extrahieren und zu verbessern.</h4>

    <!-- Dark Mode Toggle Button -->
    <button class="dark-mode-toggle" @click="toggleDarkMode">
      {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
    </button>

    <!-- Bildvorschau -->
    <div v-if="imagePreview" class="image-preview">
      <h3>Bildvorschau:</h3>
      <img :src="imagePreview" alt="Vorschau des hochgeladenen Bildes" @error="handleImageError" />
    </div>

    <!-- Bild-Upload und Button -->
    <div class="input-area">
      <input
        type="file"
        ref="fileInput"
        @change="handleImageUpload"
        accept="image/*"
        class="image-input"
      />
      <button
        @click="sendOcrRequest"
        class="send-button"
        :disabled="!selectedImage || loading"
      >
        <i class="fas fa-paper-plane"></i> OCR ausführen
      </button>
    </div>

    <!-- Anzeige der extrahierten und verbesserten Texte -->
    <div class="result-box">
      <div v-if="loading" class="loading">Verarbeite das Bild...</div>
      <div v-if="error" class="error">
        <p>Fehler: {{ error }}</p>
      </div>
      <div v-if="rawText || improvedTextHtml" class="texts-container">
        <div v-if="rawText" class="text-section raw-text-section">
          <h3>Extrahierter Text:</h3>
          <pre>{{ rawText }}</pre>
          <button class="copy-button" @click="copyText(rawText)">Kopieren</button>
        </div>
        <div v-if="improvedTextHtml" class="text-section improved-text-section">
          <h3>Verbesserter Text:</h3>
          <div v-html="improvedTextHtml"></div>
          <button class="copy-button" @click="copyText(improvedText)">Kopieren</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import DOMPurify from "dompurify";

export default {
  data() {
    return {
      selectedImage: null,
      rawText: "",
      improvedText: "",
      improvedTextHtml: "",
      imagePreview: "", // Neue Daten-Eigenschaft für die Bildvorschau
      loading: false,
      error: "",
      isDarkMode: false,
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.body.classList.toggle("dark-mode", this.isDarkMode);
      this.$el
        .querySelector(".ocr-component")
        .classList.toggle("dark-mode", this.isDarkMode);
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file && this.isAllowedFile(file.name)) {
        this.selectedImage = file;
        this.error = "";

        // Erstelle eine Vorschau des Bildes
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.error = `Ungültiges Bildformat. Erlaubt: ${[
          "png",
          "jpg",
          "jpeg",
          "gif",
          "bmp",
          "tiff",
        ].join(", ")}`;
        this.selectedImage = null;
        this.imagePreview = "";

        // Setze das Dateieingabefeld zurück, falls ungültiges Bild
        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = "";
        }
      }
    },
    handleImageError() {
      this.error = "Fehler beim Laden der Bildvorschau.";
      this.imagePreview = "";
    },
    isAllowedFile(filename) {
      const allowedExtensions = [
        "png",
        "jpg",
        "jpeg",
        "gif",
        "bmp",
        "tiff",
      ];
      const extension = filename.split(".").pop().toLowerCase();
      return allowedExtensions.includes(extension);
    },
    async sendOcrRequest() {
      if (!this.selectedImage) {
        this.error = "Bitte wähle ein gültiges Bild aus.";
        return;
      }

      this.loading = true;
      this.error = "";
      this.rawText = "";
      this.improvedText = "";
      this.improvedTextHtml = "";

      // Senden als multipart/form-data
      const formData = new FormData();
      formData.append("image", this.selectedImage);

      try {
        const response = await axios.post("http://10.10.11.11:5001/ocr", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        if (response.data.raw_text) {
          this.rawText = response.data.raw_text;
        } else {
          this.error = "Keine Rohtextantwort erhalten.";
        }

        if (response.data.improved_text) {
          this.improvedText = response.data.improved_text;
          // Konvertiere Markdown zu HTML und sichere es
          const rawHtml = marked(this.improvedText);
          this.improvedTextHtml = DOMPurify.sanitize(rawHtml);
        } else {
          this.error += " Keine verbesserte Textantwort erhalten.";
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else {
          this.error = "Ein unerwarteter Fehler ist aufgetreten.";
        }
      } finally {
        this.loading = false;
        this.selectedImage = null;
        this.imagePreview = "";
        // Setze das Dateieingabefeld zurück
        if (this.$refs.fileInput) {
          this.$refs.fileInput.value = "";
        }
      }
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
  },
};
</script>

<style scoped>
/* Grundlegende Stile für die OCR-Komponente */
.ocr-component {
  font-family: "Roboto", sans-serif;
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
.ocr-component.dark-mode {
  background-color: #1e1e1e; /* Dunkles Grau für den Hintergrund */
  border-color: #444; /* Dunkleres Grau für Ränder */
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1); /* Heller Schatten */
}

.ocr-component.dark-mode h2 {
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

.ocr-component.dark-mode .dark-mode-toggle {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

.ocr-component.dark-mode .dark-mode-toggle:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Bildvorschau */
.image-preview {
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  background-color: #fff;
  text-align: center;
}

.ocr-component.dark-mode .image-preview {
  background-color: #2a2f32;
  border-color: #444;
}

.image-preview img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 10px;
}

/* Eingabebereich */
.input-area {
  display: flex;
  gap: 10px;
}

.image-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  color: #333;
  cursor: pointer;
}

.ocr-component.dark-mode .image-input {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

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

.ocr-component.dark-mode .send-button {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

.ocr-component.dark-mode .send-button:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Ergebnis-Box */
.result-box {
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  background-color: #fff;
  max-height: 500px;
  overflow-y: auto;
}

.ocr-component.dark-mode .result-box {
  background-color: #2a2f32;
  border-color: #444;
}

/* Ladeanzeige */
.loading {
  text-align: center;
  font-weight: bold;
  color: #ffc107; /* Warmes Gelb für Ladeanzeigen */
}

/* Fehleranzeige */
.error {
  text-align: center;
  color: #dc3545; /* Auffälliges Rot für Fehler */
  font-weight: bold;
  background-color: #f8d7da; /* Helleres Rot für Fehlerhintergrund */
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #dc3545; /* Auffälliges Rot für Fehler */
}

.ocr-component.dark-mode .error {
  background-color: #721c24; /* Dunkleres Rot für Fehlerhintergrund im Dark Mode */
  color: #f8d7da; /* Helles Rot für Text im Dark Mode */
  border-color: #f5c6cb; /* Hellere Ränder für Fehler im Dark Mode */
}

/* Textabschnitte */
.texts-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
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

.ocr-component.dark-mode .raw-text-section,
.ocr-component.dark-mode .improved-text-section {
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

.ocr-component.dark-mode .raw-text-section pre {
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

.ocr-component.dark-mode .copy-button {
  background-color: #28a745;
}

.ocr-component.dark-mode .copy-button:hover {
  background-color: #218838;
}

.ocr-component.dark-mode .copy-button:active {
  background-color: #1e7e34;
}
</style>
