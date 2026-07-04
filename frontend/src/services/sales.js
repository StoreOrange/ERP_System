import { apiRequest } from "../config/api";

export function fetchCustomers(query = "", includeInactive = false) {
  const params = new URLSearchParams();
  if (query) {
    params.set("q", query);
  }
  if (includeInactive) {
    params.set("include_inactive", "true");
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return apiRequest(`/sales-api/customers${suffix}`);
}

export function createCustomer(payload) {
  return apiRequest("/sales-api/customers", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateCustomer(customerId, payload) {
  return apiRequest(`/sales-api/customers/${customerId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function fetchNextSalesInvoice() {
  return apiRequest("/sales-api/invoices/next");
}

export function createSalesInvoice(payload) {
  return apiRequest("/sales-api/invoices", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchSalesInvoices() {
  return apiRequest("/sales-api/invoices");
}

export function fetchCashCloseSummary(fecha, bodegaId = null) {
  const params = new URLSearchParams({ fecha });
  if (bodegaId) {
    params.set("bodega_id", String(bodegaId));
  }
  return apiRequest(`/sales-api/cash-close/summary?${params.toString()}`);
}

export function fetchCashClosures() {
  return apiRequest("/sales-api/cash-close");
}

export function createCashClose(payload) {
  return apiRequest("/sales-api/cash-close", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
