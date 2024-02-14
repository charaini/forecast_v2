import axios from 'axios';
import { API_DOMAIN } from './App';

const instance = axios.create({
  baseURL: `${API_DOMAIN}/api`,
});

instance.interceptors.request.use((config) => {
  const token = window.localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `JWT ${token}`;
  }

  return config;
});

export default instance;
