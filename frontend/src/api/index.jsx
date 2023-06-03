import axios from "axios";
import useUserStore from "../store/useUserStore";

export const API_URL = process.env.REACT_APP_API_URL;

const $api = axios.create({
  withCredentials: true,
  baseURL: API_URL,
});

$api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${useUserStore.getState().token}`;
  return config;
});

export default $api;
