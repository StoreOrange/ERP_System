<template>
  <section class="page-section upgrade-page">
    <div class="module-hero upgrade-hero">
      <div class="module-hero-copy">
        <p class="page-kicker">Datos y Configuraciones</p>
        <h1 class="page-title">Upgrade</h1>
        <p class="panel-text">
          Verifica cambios disponibles en Git y solicita que la VPS ejecute la actualizacion del ERP.
        </p>
      </div>

      <div class="upgrade-status-card" :class="statusClass">
        <span class="upgrade-status-dot"></span>
        <div>
          <strong>{{ statusLabel }}</strong>
          <span>{{ statusMessage }}</span>
        </div>
      </div>
    </div>

    <article class="panel-card upgrade-panel">
      <div class="panel-head">
        <div>
          <span class="products-section-kicker">Estado Git</span>
          <h3>Control de despliegue</h3>
        </div>
        <Tag :severity="tagSeverity" :value="tagLabel" />
      </div>

      <div class="upgrade-grid">
        <div class="upgrade-metric">
          <span>Rama remota</span>
          <strong>{{ status.remote_branch || "Sin configurar" }}</strong>
        </div>
        <div class="upgrade-metric">
          <span>Commit local</span>
          <strong>{{ shortHash(status.local_commit) }}</strong>
        </div>
        <div class="upgrade-metric">
          <span>Commit remoto</span>
          <strong>{{ shortHash(status.remote_commit) }}</strong>
        </div>
        <div class="upgrade-metric">
          <span>Pendientes</span>
          <strong>{{ pendingSummary }}</strong>
        </div>
      </div>

      <div class="upgrade-actions">
        <Button
          type="button"
          severity="secondary"
          variant="outlined"
          :disabled="loading || requesting"
          @click="checkForUpdates"
        >
          <i class="bi bi-arrow-clockwise"></i>
          <span>{{ loading ? "Consultando..." : "Verificar Git" }}</span>
        </Button>
        <Button
          type="button"
          severity="success"
          :disabled="requesting || status.state === 'running'"
          @click="runUpgrade"
        >
          <i class="bi bi-cloud-download"></i>
          <span>{{ requesting ? "Enviando..." : "Actualizar aplicacion" }}</span>
        </Button>
      </div>

      <div v-if="notice" class="settings-feedback settings-feedback-success">
        <i class="bi bi-check-circle-fill"></i>
        <span>{{ notice }}</span>
      </div>
      <div v-if="error" class="settings-feedback settings-feedback-error">
        <i class="bi bi-exclamation-circle-fill"></i>
        <span>{{ error }}</span>
      </div>
    </article>

    <article class="panel-card upgrade-panel">
      <div class="panel-head">
        <div>
          <span class="products-section-kicker">Registro</span>
          <h3>Ultima salida del agente</h3>
        </div>
        <Button type="button" size="small" severity="secondary" variant="outlined" @click="loadStatus">
          Recargar
        </Button>
      </div>

      <pre class="upgrade-log">{{ logText }}</pre>
    </article>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import Button from "primevue/button";
import Tag from "primevue/tag";

import { fetchUpgradeStatus, requestUpgradeCheck, requestUpgradeRun } from "../../services/upgrade";

const status = ref({});
const loading = ref(false);
const requesting = ref(false);
const notice = ref("");
const error = ref("");
let pollTimer = null;

const statusLabel = computed(() => status.value.label || "Sin estado");
const statusMessage = computed(() => status.value.message || "Configura el agente de actualizacion en la VPS.");
const statusClass = computed(() => `upgrade-status-${status.value.state || "unavailable"}`);
const tagSeverity = computed(() => {
  if (status.value.state === "pending") return "warn";
  if (status.value.state === "running") return "info";
  if (status.value.state === "error" || status.value.state === "unavailable") return "danger";
  return "success";
});
const tagLabel = computed(() => {
  if (status.value.state === "pending") return "Cambios pendientes";
  if (status.value.state === "running") return "Actualizando";
  if (status.value.state === "error") return "Error";
  if (status.value.state === "unavailable") return "No configurado";
  return "Al dia";
});
const pendingSummary = computed(() => {
  const behind = Number(status.value.behind || 0);
  if (behind > 0) return `${behind} commit(s)`;
  return status.value.pending_updates ? "Pendiente" : "Sin cambios";
});
const logText = computed(() => {
  const lines = Array.isArray(status.value.log_tail) ? status.value.log_tail : [];
  return lines.length ? lines.join("\n") : "Sin registros del agente.";
});

function shortHash(value) {
  return value ? String(value).slice(0, 8) : "-";
}

async function loadStatus() {
  loading.value = true;
  error.value = "";
  try {
    status.value = await fetchUpgradeStatus();
  } catch (err) {
    error.value = err.message || "No se pudo consultar el estado de actualizacion";
  } finally {
    loading.value = false;
  }
}

async function checkForUpdates() {
  requesting.value = true;
  error.value = "";
  notice.value = "";
  try {
    await requestUpgradeCheck();
    notice.value = "Verificacion solicitada. El estado se actualizara en unos segundos.";
    setTimeout(loadStatus, 2500);
  } catch (err) {
    error.value = err.message || "No se pudo solicitar la verificacion";
  } finally {
    requesting.value = false;
  }
}

async function runUpgrade() {
  const confirmed = window.confirm("La VPS descargara cambios de Git y reiniciara los contenedores del ERP. Continuar?");
  if (!confirmed) return;

  requesting.value = true;
  error.value = "";
  notice.value = "";
  try {
    await requestUpgradeRun();
    notice.value = "Actualizacion solicitada. La app puede reconectarse durante el reinicio.";
    setTimeout(loadStatus, 2500);
  } catch (err) {
    error.value = err.message || "No se pudo solicitar la actualizacion";
  } finally {
    requesting.value = false;
  }
}

onMounted(() => {
  loadStatus();
  pollTimer = window.setInterval(loadStatus, 15000);
});

onBeforeUnmount(() => {
  if (pollTimer) {
    window.clearInterval(pollTimer);
  }
});
</script>

<style scoped>
.upgrade-page {
  display: grid;
  gap: 1rem;
}

.upgrade-hero {
  align-items: center;
}

.upgrade-status-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: min(100%, 22rem);
  padding: 0.95rem 1rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: var(--erp-surface);
}

.upgrade-status-card strong,
.upgrade-status-card span {
  display: block;
}

.upgrade-status-card strong {
  color: var(--erp-text);
}

.upgrade-status-card span:last-child {
  color: var(--erp-text-muted);
  font-size: 0.82rem;
}

.upgrade-status-dot {
  width: 0.85rem;
  height: 0.85rem;
  border-radius: 999px;
  background: var(--erp-text-muted);
}

.upgrade-status-ready .upgrade-status-dot {
  background: var(--erp-success);
}

.upgrade-status-pending .upgrade-status-dot {
  background: var(--erp-warning);
}

.upgrade-status-running .upgrade-status-dot {
  background: #3f6fbd;
}

.upgrade-status-error .upgrade-status-dot,
.upgrade-status-unavailable .upgrade-status-dot {
  background: var(--erp-danger);
}

.upgrade-panel {
  display: grid;
  gap: 1rem;
}

.upgrade-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.75rem;
}

.upgrade-metric {
  min-width: 0;
  padding: 0.8rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: var(--erp-surface-muted);
}

.upgrade-metric span,
.upgrade-metric strong {
  display: block;
}

.upgrade-metric span {
  color: var(--erp-text-muted);
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
}

.upgrade-metric strong {
  margin-top: 0.3rem;
  overflow: hidden;
  color: var(--erp-text);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upgrade-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  justify-content: flex-end;
}

.upgrade-actions :deep(.p-button) {
  gap: 0.45rem;
}

.upgrade-log {
  min-height: 14rem;
  max-height: 26rem;
  margin: 0;
  padding: 0.85rem;
  overflow: auto;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: #151820;
  color: #d7e0f0;
  font-size: 0.78rem;
  line-height: 1.55;
  white-space: pre-wrap;
}

@media (max-width: 980px) {
  .upgrade-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .upgrade-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .upgrade-actions {
    justify-content: stretch;
  }

  .upgrade-actions :deep(.p-button) {
    width: 100%;
  }
}
</style>
