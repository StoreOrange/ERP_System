import { apiRequest } from "../config/api";

export function fetchUpgradeStatus() {
  return apiRequest("/upgrade/status");
}

export function requestUpgradeCheck() {
  return apiRequest("/upgrade/check", {
    method: "POST",
  });
}

export function requestUpgradeRun() {
  return apiRequest("/upgrade/run", {
    method: "POST",
  });
}
