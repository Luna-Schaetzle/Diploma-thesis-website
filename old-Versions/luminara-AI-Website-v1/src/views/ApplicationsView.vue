<!-- src/views/ApplicationsView.vue -->
<template>
  <div class="applications-view" :class="{ 'dark-mode': isDarkMode }">
    <!-- Sidebar -->
    <div class="sidebar">
      <header>
        <h1>Luminara AI v.0.4 (experimental)</h1>
      </header>

      <!-- Navigation als Sidebar -->
      <nav>
        <router-link
          to="/applications/ollama"
          class="sidebar-link"
          active-class="active"
        >
          Chat mit Ollama 
        </router-link>
        <router-link
          to="/applications/chat"
          class="sidebar-link"
          active-class="active"
        >
          Chat 
        </router-link>
        <router-link
          to="/applications/chatgpt"
            class="sidebar-link"
            active-class="active"
        >
            Chat GPT
        </router-link>

        <!--router-link
          to="/applications/image"
          class="sidebar-link"
          active-class="active"
        >
          Bildgenerierung
        </router-link>
        <router-link
          to="/applications/gallery"
          class="sidebar-link"
          active-class="active"
        >
          Galerie
        </router-link-->
      </nav>
    </div>

    <!-- Anzeige der aktiven Unterkomponente -->
    <div class="component-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApplicationsView',
  data() {
    return {
      isDarkMode: false, // Dark Mode Status
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      // Optional: Speichere den Dark Mode Status im Local Storage
      localStorage.setItem('isDarkMode', this.isDarkMode);
    },
  },
  created() {
    // Optional: Lade den Dark Mode Status aus dem Local Storage
    const savedMode = localStorage.getItem('isDarkMode');
    if (savedMode !== null) {
      this.isDarkMode = JSON.parse(savedMode);
    }
  },
};
</script>

<style scoped>
/* Stile ähnlich wie zuvor, angepasst für Router-Links */

.applications-view {
  display: flex;
  flex-direction: row;
  height: 100%;
}

.dark-mode {
  background-color: #121212;
  color: #f0f0f0;
}

/* Sidebar */
.sidebar {
  width: 250px;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.applications-view.dark-mode .sidebar {
  background-color: #1e1e1e;
  box-shadow: 2px 0 5px rgba(255, 255, 255, 0.1);
}

.sidebar header h1 {
  font-size: 1.5rem;
  color: #2c3e50;
  transition: color 0.3s;
}

.applications-view.dark-mode .sidebar header h1 {
  color: #bb86fc;
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar-link {
  padding: 10px 15px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  text-decoration: none;
  transition: background-color 0.3s, transform 0.2s;
  cursor: pointer;
}

.sidebar-link:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.sidebar-link.active {
  background-color: #2ecc71;
}

.applications-view.dark-mode .sidebar-link {
  background-color: #1e90ff;
}

.applications-view.dark-mode .sidebar-link.active {
  background-color: #27ae60;
}

.applications-view.dark-mode .sidebar-link:hover {
  background-color: #1c86ee;
}

/* Komponenten-Anzeige */
.component-container {
  flex: 1;
  max-width: 800px;
  background-color: #ffffff;
  padding: 20px;
  margin-left: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

.applications-view.dark-mode .component-container {
  background-color: #1e1e1e;
  box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
}

.component-container router-view {
  transition: opacity 0.5s ease-in-out;
}

/* Responsive Anpassungen */
@media (max-width: 900px) {
  .applications-view {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    flex-direction: row;
    overflow-x: auto;
  }

  .sidebar nav {
    flex-direction: row;
    gap: 5px;
  }

  .component-container {
    margin-left: 0;
    margin-top: 20px;
    max-width: 100%;
  }
}
</style>