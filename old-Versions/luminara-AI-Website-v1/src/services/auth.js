// src/services/auth.js
import axios from 'axios';

const API_URL = 'http://localhost:5000/api/auth'; // Passen Sie die URL an Ihr Backend an

class AuthService {
  async register(user) {
    const response = await axios.post(`${API_URL}/register`, user);
    if (response.data.token) {
      this.setToken(response.data.token);
    }
    return response.data;
  }

  async login(user) {
    const response = await axios.post(`${API_URL}/login`, user);
    if (response.data.token) {
      this.setToken(response.data.token);
    }
    return response.data;
  }

  logout() {
    localStorage.removeItem('token');
  }

  setToken(token) {
    localStorage.setItem('token', token);
  }

  getToken() {
    return localStorage.getItem('token');
  }

  isAuthenticated() {
    return !!this.getToken();
  }
}

export default new AuthService();
