import axios from 'axios';
import BASE_URL from './baseUrl'; 


export const login = async ({ username, password}) => {
  const client_id = "1n7HunZixhvfW6ZfAO1eWvBT9Kuksk68GlDjDYiK";
  const client_secret = "HoEjHsI2hikoPFmsN45VtcTtzw3z7PJ043VLC2RB2i0MDMag4dRomSzqkGUMZ8XsbsWrCge89FgkYj8isqavt7M8bR1eAGrowyPGOpWECXWWQmA40XBtKa78aY1lLym1";
  const grant_type = "password";
  const response = await axios.post(`${BASE_URL}/o/token/`, { username, password, client_id, client_secret, grant_type});
  console.log(response.data);
  return response.data;
};

export const register = async (userData) => {
  const response = await axios.post(`${BASE_URL}/api/users/`, userData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  console.log(response.data);

  return response.data;
};

export const getCurrentUser = async (token) => {
  const response = await axios.get(`${BASE_URL}/api/users/current-user/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  console.log(response.data);
  return response.data;
};
