<template>
  <div class="bg-gray-100 min-h-screen">
    <!-- Header / Hero Section -->
    <header class="bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-20 relative overflow-hidden">
      <div class="container mx-auto text-center relative z-10">
        <h1 class="text-5xl font-bold mb-4 animate-fade-in">Luminara Schüler-KI-Plattform</h1>
        <p class="text-xl animate-fade-in-delayed">
          Deine Unterstützung beim Lernen mit leistungsstarken KI-Tools
        </p>
        <div class="mt-8">
          <router-link
            to="/register"
            class="button bg-white text-blue-500 px-6 py-3 rounded-full font-semibold hover:bg-gray-200 transition">
            Jetzt Registrieren
          </router-link>
        </div>
      </div>
      <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-blue-400 to-indigo-500 opacity-50 blur-md z-0"></div>
    </header>

    <!-- Beschreibung -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <h2 class="section-title">Beschreibung</h2>
        <p class="section-description">
          Die Schüler-KI-Plattform ist eine webbasierte Anwendung, die es Schülern ermöglicht, sich anzumelden und mit verschiedenen Künstlichen Intelligenzen (KI) zu interagieren. Die Plattform kombiniert die Nutzung der ChatGPT-API mit unbegrenzten lokalen KI-Modellen wie Ollama, die auf dem Schulserver betrieben werden. Ziel ist es, den Schülern vielseitige Unterstützung beim Lernen und bei der Bearbeitung von Aufgaben zu bieten.
        </p>
      </div>
    </section>

    <!-- Funktionen -->
    <section class="bg-white py-16">
      <div class="container mx-auto px-4">
        <h2 class="section-title">Funktionen</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <FeatureCard title="Programmierbot" description="Unterstützung beim Programmieren durch Beantwortung von Fragen und Bereitstellung von Codebeispielen." icon="👨‍💻"/>
          <FeatureCard title="OCR (Bild zu Mitschrift)" description="Konvertierung von Bildern in Text, um handschriftliche Notizen oder gedruckte Dokumente digital verfügbar zu machen." icon="📄"/>
          <FeatureCard title="Allgemeiner Chatbot" description="Ein angepasster Chatbot mit einem speziellen System-Prompt für allgemeine Anfragen und Konversationen." icon="💬"/>
          <FeatureCard title="Bilderkennung" description="Analyse und Lösung von Aufgaben anhand von hochgeladenen Bildern." icon="🖼️"/>
          <FeatureCard title="Mathe-Bot" description="Unterstützung bei mathematischen Problemen und Aufgabenlösungen." icon="➗"/>
          <FeatureCard title="Chatten mit API" description="Integration von ChatGPT und Claude AI mit Token-Limitierungen für erweiterte Konversationsmöglichkeiten." icon="🔗"/>
          <FeatureCard title="Testvorbereitung" description="Generierung von Fragen zur Vorbereitung auf Tests, eventuell mit einem Karteikartensystem zur effektiven Wiederholung." icon="📚"/>
        </div>
      </div>
    </section>

    <!-- Konto-Modell -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <h2 class="section-title">Konto-Modell</h2>
        <div class="flex flex-col md:flex-row justify-center items-center gap-8">
          <AccountCard 
            title="Student-Accounts" 
            description="Jeder Schüler erhält pro Monat eine bestimmte Anzahl an Premium-Token, die zum Promten der leistungsstarken KI-Modelle wie ChatGPT und Claude AI verwendet werden können. Nicht genutzte Token werden auf den nächsten Monat übertragen."
            icon="👩‍🎓"
          />
          <AccountCard 
            title="Admin- und Dev-Accounts" 
            description="Diese Konten besitzen unbegrenzte Token, um umfassende Verwaltungs- und Entwicklungsaufgaben zu unterstützen. Admins haben zusätzliche Rechte zur Verwaltung von Benutzerkonten, Token-Verteilungen und Systemkonfigurationen."
            icon="🛠️"
          />
          <AccountCard 
            title="Student+ Accounts" 
            description="Diese erweiterten Schülerkonten bieten eine größere Menge an Token, um intensivere Nutzung der KI-Dienste zu ermöglichen. Antragstellung erforderlich."
            icon="⭐"
          />
        </div>
      </div>
    </section>

    <!-- Technologie-Stack -->
    <section class="bg-white py-16">
      <div class="container mx-auto px-4">
        <h2 class="section-title">Technologie-Stack</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <TechCard title="Frontend" description="Vue.js" icon="🌐"/>
          <TechCard title="Backend" description="Node.js, Express" icon="⚙️"/>
          <TechCard title="KI-Modelle" description="ChatGPT API, Ollama, Claude AI" icon="🤖"/>
          <TechCard title="Weitere Technologien" description="OCR-Tools (z.B. Tesseract), Bildverarbeitungslibraries (z.B. TensorFlow, OpenCV)" icon="🛠️"/>
          <TechCard title="Datenbank" description="Firebase" icon="💾"/>
        </div>
      </div>
    </section>

    <!-- Kontakt -->
    <section class="py-16">
      <div class="container mx-auto px-4 text-center">
        <h2 class="section-title">Kontakt</h2>
        <p class="section-description">
          Bei Fragen oder Anregungen kannst du dich gerne an mich wenden:
        </p>
        <p class="text-lg text-gray-700 mb-2">
          <strong>E-Mail:</strong> <a href="mailto:LuminaraAI.Website@gmail.com" class="text-blue-500 underline">LuminaraAI.Website@gmail.com</a>
        </p>
        <p class="text-lg text-gray-700">
          <strong>GitHub:</strong> <a href="https://github.com/Luna-Schaetzle" class="text-blue-500 underline" target="_blank">Luna-Schaetzle</a>
        </p>
      </div>
    </section>
  </div>
</template>


<script>
import FeatureCard from './FeatureCard.vue';
import AccountCard from './AccountCard.vue';
import TechCard from './TechCard.vue';

export default {
  name: 'HomeView',
  components: {
    FeatureCard,
    AccountCard,
    TechCard
  }
}
</script>
<style>
/* Globale Animationen */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in-delayed {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header Animationen */
.animate-fade-in {
  animation: fade-in 1s ease-out forwards;
}

.animate-fade-in-delayed {
  animation: fade-in-delayed 1s ease-out forwards;
  animation-delay: 0.3s;
}

/* Allgemeine Stile */
body {
  font-family: 'Inter', sans-serif;
  color: #333;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

.section-title {
  font-size: 1.75rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1.5rem;
  position: relative;
}

.section-title::after {
  content: '';
  width: 50px;
  height: 4px;
  background-color: #4f46e5;
  display: block;
  margin: 1rem auto 0;
}

.section-description {
  line-height: 1.75;
  color: #4b5563;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

a {
  color: #4f46e5;
  text-decoration: none;
}

a:hover {
  color: #6b21a8;
  text-decoration: underline;
}

/* Buttons */
.button {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  color: #fff;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 999px;
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.button:hover {
  background: linear-gradient(to right, #4338ca, #6b21a8);
  transform: scale(1.05);
}

/* Karten Stile */
.grid {
  display: grid;
  gap: 2rem;
}

.card {
  background: linear-gradient(to bottom right, #ffffff, #f3f4f6);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-8px);
  background: linear-gradient(to bottom right, #f9fafb, #e5e7eb);
}

/* Footer */
footer {
  font-size: 0.875rem;
  line-height: 1.5;
}

footer a {
  color: #ffffff;
}

footer a:hover {
  color: #e0e7ff;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 0 1.5rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
