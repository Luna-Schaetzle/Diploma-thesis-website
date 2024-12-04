<template>
    <div class="image-generator">
      <h1>Bildgenerator</h1>
      <div class="token-info">
        <p>Verbleibende Tokens: <strong>{{ tokens }}</strong></p>
      </div>
  
      <div class="input-area">
        <input
          v-model="prompt"
          placeholder="Gib einen Prompt ein (z. B. 'A cute baby sea otter')"
          class="prompt-input"
        />
        <button @click="generateImage" :disabled="loading || tokens < 5" class="generate-button">
          Bild generieren (5 Tokens)
        </button>
      </div>
  
      <div v-if="loading" class="loading">Bild wird generiert...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
  
      <div class="image-display" v-if="imageUrl">
        <img :src="imageUrl" alt="Generated Image" class="generated-image" />
      </div>
    </div>
  </template>

<script>
import OpenAI from "openai";
import { OPENAI_API_KEY } from "../secrets"
import { getAuth } from "firebase/auth";
import { getFirestore, doc, getDoc, updateDoc } from "firebase/firestore";

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY,
  dangerouslyAllowBrowser: true,
});

export default {
  data() {
    return {
      prompt: "", // Eingabe für das Bild
      imageUrl: "", // URL des generierten Bildes
      tokens: 0, // Verfügbare Tokens
      loading: false,
      error: "",
      success: "",
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
    async generateImage() {
      if (this.prompt.trim() === "") {
        this.error = "Prompt darf nicht leer sein!";
        return;
      }

      if (this.tokens < 5) {
        this.error = "Nicht genug Tokens! 5 Tokens erforderlich.";
        return;
      }

      this.loading = true;
      this.error = "";
      this.success = "";

      try {
        const auth = getAuth();
        const db = getFirestore();
        const currentUser = auth.currentUser;

        if (currentUser) {
          const userRef = doc(db, "users", currentUser.uid);
          const userDoc = await getDoc(userRef);

          if (userDoc.exists()) {
            const currentTokens = userDoc.data().tokens;

            if (currentTokens >= 5) {
              // Anfrage an die OpenAI-API für die Bildgenerierung
              const imageResponse = await openai.images.generate({
                model: "dall-e-2",
                prompt: this.prompt,
                size: "1024x1024",
                quality: "standard",
              });

              this.imageUrl = imageResponse.data[0].url;
              this.success = "Bild erfolgreich generiert!";

              // Token-Verbrauch aktualisieren
              await updateDoc(userRef, {
                tokens: currentTokens - 5,
              });

              this.tokens = currentTokens - 5; // Lokale Anzeige aktualisieren
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
        this.error = "Fehler bei der Bildgenerierung: " + err.message;
      } finally {
        this.loading = false;
        this.prompt = ""; // Eingabe zurücksetzen
      }
    },
  },
};
</script>

<style scoped>
.image-generator {
  font-family: "Roboto", Arial, sans-serif;
  max-width: 600px;
  margin: 40px auto;
  padding: 25px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: linear-gradient(to bottom, #ffffff, #f0f0f0);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.token-info {
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
}

.input-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.prompt-input {
  width: 90%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: border 0.3s, box-shadow 0.3s;
}

.prompt-input:focus {
  border: 2px solid #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.4);
}

.generate-button {
  padding: 12px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
}

.generate-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  box-shadow: none;
}

.generate-button:hover:not(:disabled) {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.loading {
  color: #ff9800;
  margin-top: 10px;
  font-weight: bold;
}

.error {
  color: #e74c3c;
  margin-top: 10px;
  font-weight: bold;
}

.success {
  color: #27ae60;
  margin-top: 10px;
  font-weight: bold;
}

.image-display {
  margin-top: 30px;
  text-align: center;
}

.generated-image {
  max-width: 100%;
  height: auto;
  border: 2px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.generated-image:hover {
  transform: scale(1.05);
}
</style>
