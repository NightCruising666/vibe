import axios from "axios";

const http = axios.create({
  baseURL: "/api",
  timeout: 8000,
});

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const message = err.response?.data?.message || err.message;
    return Promise.reject(new Error(message));
  },
);

export default http;
