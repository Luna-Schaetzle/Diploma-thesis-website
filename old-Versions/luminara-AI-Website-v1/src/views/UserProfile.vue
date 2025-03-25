<!-- src/views/UserProfile.vue -->
<template>
    <div class="profile">
      <h2>Mein Profil</h2>
      <div v-if="user">
        <p><strong>Benutzername:</strong> {{ user.username }}</p>
        <p><strong>E-Mail:</strong> {{ user.email }}</p>
        <p><strong>Registriert am:</strong> {{ user.created_at }}</p>
      </div>
      <p v-else>Loading...</p>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import AuthService from '../services/auth';
  
  export default {
    name: 'UserProfile', // Aktualisierter Name
    data() {
      return {
        user: null,
        error: ''
      };
    },
    methods: {
      async fetchProfile() {
        try {
          const response = await axios.get('/user/profile');
          this.user = response.data;
        } catch (err) {
          this.error = err.response?.data?.message || 'Fehler beim Laden des Profils.';
        }
      },
      logout() {
        AuthService.logout();
        this.$router.push('/login');
      }
    },
    created() {
      this.fetchProfile();
    }
  };
  </script>
  
  <style scoped>
  .profile {
    max-width: 600px;
    margin: auto;
  }
  .error {
    color: red;
  }
  </style>
  