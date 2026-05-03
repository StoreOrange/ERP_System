import { apiRequest } from "../config/api";

export function loginUser(payload) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchCurrentUser() {
  return apiRequest("/auth/me");
}

export function storeSession(data) {
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("currentUser", JSON.stringify(data.user));
}

export function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("currentUser");
}

export function readStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("currentUser") || "null");
  } catch {
    return null;
  }
}
