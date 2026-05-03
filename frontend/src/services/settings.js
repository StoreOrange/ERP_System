import { API_BASE_URL, apiRequest } from "../config/api";

const SETTINGS_STORAGE_KEY = "businessSettings";

export function buildAssetUrl(path) {
  if (!path) {
    return "";
  }

  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }

  return `${API_BASE_URL}${path}`;
}

export function readStoredBusinessSettings() {
  try {
    return JSON.parse(localStorage.getItem(SETTINGS_STORAGE_KEY) || "null");
  } catch {
    return null;
  }
}

export function storeBusinessSettings(settings) {
  localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
  window.dispatchEvent(new CustomEvent("business-settings-updated", { detail: settings }));
}

export function applyBusinessBranding(settings) {
  if (!settings) {
    return;
  }

  const businessLabel = settings.trade_name || settings.business_name;
  const titleLabel = settings.app_title || businessLabel;

  document.title = titleLabel
    ? `${titleLabel} | ERP`
    : "ERP System";

  const faviconHref = buildAssetUrl(settings.logo_favicon);
  if (!faviconHref) {
    return;
  }

  let favicon = document.querySelector("link[rel='icon']");
  if (!favicon) {
    favicon = document.createElement("link");
    favicon.setAttribute("rel", "icon");
    document.head.appendChild(favicon);
  }

  favicon.setAttribute("href", faviconHref);
}

export async function fetchPublicBusinessSettings() {
  const settings = await apiRequest("/settings/business/public");
  storeBusinessSettings(settings);
  applyBusinessBranding(settings);
  return settings;
}

export async function fetchBusinessSettings() {
  const settings = await apiRequest("/settings/business");
  storeBusinessSettings(settings);
  applyBusinessBranding(settings);
  return settings;
}

export async function saveBusinessSettings(payload) {
  const settings = await apiRequest("/settings/business", {
    method: "PUT",
    body: payload,
  });
  storeBusinessSettings(settings);
  applyBusinessBranding(settings);
  return settings;
}

export async function fetchCompanyEnvironments() {
  return apiRequest("/settings/environments");
}

export async function createCompanyEnvironment(payload) {
  return apiRequest("/settings/environments", {
    method: "POST",
    body: payload,
  });
}

export async function updateCompanyEnvironment(environmentId, payload) {
  return apiRequest(`/settings/environments/${environmentId}`, {
    method: "PUT",
    body: payload,
  });
}

export async function activateCompanyEnvironment(environmentId) {
  return apiRequest(`/settings/environments/${environmentId}/activate`, {
    method: "PATCH",
  });
}
