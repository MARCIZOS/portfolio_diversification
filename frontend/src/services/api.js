import axios from 'axios';

// Use relative API path in production (deployed on same domain)
// Use localhost for development
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth Services
export const loginUser = async (username, password) => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

export const signupUser = async (username, email, password) => {
  const response = await api.post('/auth/signup', { username, email, password });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Portfolio Services
export const analyzePortfolio = async (assets, debugRag = false) => {
  const response = await api.post('/portfolio', {
    assets,
    debug_rag: debugRag
  });
  return response.data;
};

export default api;
