<template>
  <section class="page-section upgrade-page">
    <div class="module-hero upgrade-hero">
      <div class="module-hero-copy">
        <p class="page-kicker">Datos y Configuraciones</p>
        <h1 class="page-title">Centro de Actualizaciones</h1>
        <p class="panel-text">
          Revisa cambios publicados en Git y actualiza la aplicacion en la VPS con seguimiento del proceso.
        </p>
      </div>

      <div class="upgrade-orbital-card" :class="statusClass">
        <div class="upgrade-orbit" :class="{ active: isBusy }">
          <i class="bi" :class="statusIcon"></i>
        </div>
        <div>
          <strong>{{ statusLabel }}</strong>
          <span>{{ statusMessage }}</span>
        </div>
      </div>
    </div>

    <div v-if="notice || error" class="upgrade-message" :class="{ error: Boolean(error) }">
      <i class="bi" :class="error ? 'bi-exclamation-circle-fill' : 'bi-check-circle-fill'"></i>
      <span>{{ error || notice }}</span>
    </div>

    <section v-if="isBusy || reconnectCountdown > 0" class="panel-card upgrade-progress-card">
      <div class="upgrade-progress-head">
        <div class="upgrade-hourglass">
          <i class="bi bi-hourglass-split"></i>
        </div>
        <div>
          <span class="products-section-kicker">Actualizacion en proceso</span>
          <h3>{{ progressTitle }}</h3>
          <p class="panel-text">
            La aplicacion puede reiniciarse. Esta pantalla consultara el estado automaticamente.
          </p>
        </div>
        <strong class="upgrade-countdown">{{ reconnectCountdown || "..." }}s</strong>
      </div>
      <div class="upgrade-progress-track">
        <span :style="{ width: `${progressPercent}%` }"></span>
      </div>
    </section>

    <div class="upgrade-layout">
      <article class="panel-card upgrade-panel upgrade-control-panel">
        <div class="panel-head">
          <div>
            <span class="products-section-kicker">Estado Git</span>
            <h3>Control de despliegue</h3>
          </div>
          <Tag :severity="tagSeverity" :value="tagLabel" />
        </div>

        <div class="upgrade-grid">
          <div class="upgrade-metric">
            <i class="bi bi-git"></i>
            <span>Rama remota</span>
            <strong>{{ status.remote_branch || "Sin configurar" }}</strong>
          </div>
          <div class="upgrade-metric">
            <i class="bi bi-pc-display"></i>
            <span>Version VPS</span>
            <strong>{{ shortHash(status.local_commit) }}</strong>
          </div>
          <div class="upgrade-metric">
            <i class="bi bi-cloud-check"></i>
            <span>Version Git</span>
            <strong>{{ shortHash(status.remote_commit) }}</strong>
          </div>
          <div class="upgrade-metric" :class="{ pending: Number(status.behind || 0) > 0 }">
            <i class="bi bi-arrow-down-circle"></i>
            <span>Pendientes</span>
            <strong>{{ pendingSummary }}</strong>
          </div>
        </div>

        <div class="upgrade-steps">
          <div v-for="step in steps" :key="step.key" class="upgrade-step" :class="step.className">
            <i class="bi" :class="step.icon"></i>
            <div>
              <strong>{{ step.label }}</strong>
              <span>{{ step.caption }}</span>
            </div>
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
      </article>

      <article class="panel-card upgrade-panel upgrade-audit-panel">
        <div class="panel-head">
          <div>
            <span class="products-section-kicker">Auditoria</span>
            <h3>Actividad reciente</h3>
          </div>
          <Button type="button" size="small" severity="secondary" variant="outlined" @click="loadStatus">
            Recargar
          </Button>
        </div>

        <div class="upgrade-audit-list">
          <article v-for="entry in auditEntries" :key="entry.id" class="upgrade-audit-row">
            <i class="bi" :class="entry.icon"></i>
            <div>
              <strong>{{ entry.title }}</strong>
              <span>{{ entry.detail }}</span>
            </div>
          </article>
        </div>
      </article>
    </div>

    <article class="panel-card upgrade-panel">
      <div class="panel-head">
        <div>
          <span class="products-section-kicker">Registro tecnico</span>
          <h3>Salida del agente</h3>
        </div>
        <Tag severity="contrast" :value="`${logLines.length} lineas`" />
      </div>

      <div class="upgrade-log">
        <div v-if="!logLines.length" class="upgrade-log-empty">
          Sin registros del agente.
        </div>
        <div v-for="(line, index) in logLines" v-else :key="`${index}-${line}`" class="upgrade-log-line">
          <span>{{ String(index + 1).padStart(2, "0") }}</span>
          <p>{{ line }}</p>
        </div>
      </div>
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
const reconnectCountdown = ref(0);
const progressPercent = ref(0);
let pollTimer = null;
let countdownTimer = null;

const isBusy = computed(() => requesting.value || status.value.state === "running");
const statusLabel = computed(() => status.value.label || "Sin estado");
const statusMessage = computed(() => status.value.message || "Configura el agente de actualizacion en la VPS.");
const statusClass = computed(() => `upgrade-status-${status.value.state || "unavailable"}`);
const statusIcon = computed(() => {
  if (status.value.state === "pending") return "bi-cloud-arrow-down-fill";
  if (status.value.state === "running") return "bi-arrow-repeat";
  if (status.value.state === "error" || status.value.state === "unavailable") return "bi-exclamation-triangle-fill";
  return "bi-shield-check";
});
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
const logLines = computed(() => (Array.isArray(status.value.log_tail) ? status.value.log_tail : []));
const progressTitle = computed(() =>
  reconnectCountdown.value > 0 ? "Esperando reconexion del ERP" : "Preparando solicitud de actualizacion",
);
const steps = computed(() => [
  {
    key: "git",
    label: "Git verificado",
    caption: status.value.remote_commit ? `Remoto ${shortHash(status.value.remote_commit)}` : "Pendiente de lectura",
    icon: "bi-git",
    className: status.value.remote_commit ? "done" : "",
  },
  {
    key: "pending",
    label: "Cambios detectados",
    caption: pendingSummary.value,
    icon: "bi-cloud-arrow-down",
    className: Number(status.value.behind || 0) > 0 ? "active" : "done",
  },
  {
    key: "deploy",
    label: "Despliegue VPS",
    caption: status.value.state === "running" ? "Reiniciando contenedores" : "Listo para ejecutar",
    icon: "bi-box-arrow-up",
    className: status.value.state === "running" ? "active" : "",
  },
]);
const auditEntries = computed(() => {
  const entries = [
    {
      id: "state",
      icon: status.value.state === "error" ? "bi-x-circle-fill" : "bi-info-circle-fill",
      title: statusLabel.value,
      detail: statusMessage.value,
    },
    {
      id: "checked",
      icon: "bi-clock-history",
      title: "Ultima verificacion",
      detail: status.value.checked_at ? formatDate(status.value.checked_at) : "Sin lectura registrada",
    },
    {
      id: "branch",
      icon: "bi-diagram-3-fill",
      title: "Rama monitoreada",
      detail: status.value.remote_branch || "No configurada",
    },
  ];

  logLines.value.slice(-3).reverse().forEach((line, index) => {
    entries.push({
      id: `log-${index}`,
      icon: "bi-journal-text",
      title: "Evento del agente",
      detail: line,
    });
  });

  return entries;
});

function shortHash(value) {
  return value ? String(value).slice(0, 8) : "-";
}

function formatDate(value) {
  try {
    return new Intl.DateTimeFormat("es-NI", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

function startReconnectCountdown(seconds = 45) {
  reconnectCountdown.value = seconds;
  progressPercent.value = 8;
  if (countdownTimer) {
    window.clearInterval(countdownTimer);
  }
  countdownTimer = window.setInterval(() => {
    reconnectCountdown.value = Math.max(reconnectCountdown.value - 1, 0);
    progressPercent.value = Math.min(96, Math.round(((seconds - reconnectCountdown.value) / seconds) * 100));
    if (reconnectCountdown.value <= 0) {
      window.clearInterval(countdownTimer);
      countdownTimer = null;
      progressPercent.value = 100;
      loadStatus();
    }
  }, 1000);
}

async function loadStatus() {
  loading.value = true;
  error.value = "";
  try {
    status.value = await fetchUpgradeStatus();
    if (status.value.state !== "running" && reconnectCountdown.value <= 0) {
      progressPercent.value = status.value.state === "ready" ? 100 : 0;
    }
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
    startReconnectCountdown();
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
  if (countdownTimer) {
    window.clearInterval(countdownTimer);
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

.upgrade-orbital-card {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  min-width: min(100%, 25rem);
  padding: 1rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: linear-gradient(135deg, #ffffff, var(--erp-surface-muted));
}

.upgrade-orbital-card strong,
.upgrade-orbital-card span {
  display: block;
}

.upgrade-orbital-card strong {
  color: var(--erp-text);
  font-size: 1rem;
}

.upgrade-orbital-card span {
  margin-top: 0.18rem;
  color: var(--erp-text-muted);
  font-size: 0.82rem;
}

.upgrade-orbit {
  position: relative;
  display: grid;
  flex: 0 0 auto;
  width: 3.2rem;
  height: 3.2rem;
  place-items: center;
  border: 1px solid rgba(117, 87, 168, 0.18);
  border-radius: 50%;
  background: #ffffff;
  color: var(--erp-primary);
  font-size: 1.35rem;
}

.upgrade-orbit::after {
  position: absolute;
  inset: -0.3rem;
  content: "";
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  opacity: 0.55;
}

.upgrade-orbit.active::after {
  animation: upgrade-spin 1.1s linear infinite;
}

.upgrade-status-pending .upgrade-orbit {
  color: var(--erp-warning);
}

.upgrade-status-running .upgrade-orbit {
  color: #3f6fbd;
}

.upgrade-status-error .upgrade-orbit,
.upgrade-status-unavailable .upgrade-orbit {
  color: var(--erp-danger);
}

.upgrade-message,
.upgrade-progress-card,
.upgrade-panel {
  border-radius: 8px;
}

.upgrade-message {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(61, 122, 91, 0.24);
  background: rgba(61, 122, 91, 0.08);
  color: var(--erp-success);
  font-weight: 750;
}

.upgrade-message.error {
  border-color: rgba(181, 84, 84, 0.24);
  background: rgba(181, 84, 84, 0.08);
  color: var(--erp-danger);
}

.upgrade-progress-card {
  display: grid;
  gap: 0.9rem;
}

.upgrade-progress-head {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 0.85rem;
}

.upgrade-hourglass {
  display: grid;
  width: 3.3rem;
  height: 3.3rem;
  place-items: center;
  border-radius: 8px;
  background: var(--erp-primary-soft);
  color: var(--erp-primary-strong);
  font-size: 1.35rem;
  animation: upgrade-pulse 1.5s ease-in-out infinite;
}

.upgrade-countdown {
  display: grid;
  min-width: 4.4rem;
  min-height: 3rem;
  place-items: center;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: #ffffff;
  color: var(--erp-primary-strong);
  font-size: 1.1rem;
}

.upgrade-progress-track {
  height: 0.55rem;
  overflow: hidden;
  border-radius: 999px;
  background: var(--erp-surface-soft);
}

.upgrade-progress-track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--erp-primary), #3f6fbd, var(--erp-success));
  transition: width 0.35s ease;
}

.upgrade-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(22rem, 0.65fr);
  gap: 1rem;
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
  padding: 0.85rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: #ffffff;
}

.upgrade-metric.pending {
  border-color: rgba(168, 114, 61, 0.32);
  background: rgba(168, 114, 61, 0.08);
}

.upgrade-metric i,
.upgrade-metric span,
.upgrade-metric strong {
  display: block;
}

.upgrade-metric i {
  margin-bottom: 0.55rem;
  color: var(--erp-primary);
  font-size: 1.15rem;
}

.upgrade-metric span {
  color: var(--erp-text-muted);
  font-size: 0.7rem;
  font-weight: 850;
  text-transform: uppercase;
}

.upgrade-metric strong {
  margin-top: 0.3rem;
  overflow: hidden;
  color: var(--erp-text);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upgrade-steps {
  display: grid;
  gap: 0.55rem;
}

.upgrade-step,
.upgrade-audit-row {
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  padding: 0.75rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: #ffffff;
}

.upgrade-step i,
.upgrade-audit-row i {
  color: var(--erp-primary);
  font-size: 1rem;
}

.upgrade-step strong,
.upgrade-step span,
.upgrade-audit-row strong,
.upgrade-audit-row span {
  display: block;
}

.upgrade-step span,
.upgrade-audit-row span {
  margin-top: 0.15rem;
  color: var(--erp-text-muted);
  font-size: 0.78rem;
  line-height: 1.45;
}

.upgrade-step.done i {
  color: var(--erp-success);
}

.upgrade-step.active {
  border-color: rgba(63, 111, 189, 0.28);
  background: rgba(63, 111, 189, 0.07);
}

.upgrade-step.active i {
  animation: upgrade-spin 1.2s linear infinite;
  color: #3f6fbd;
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

.upgrade-audit-list {
  display: grid;
  gap: 0.55rem;
  max-height: 28rem;
  overflow: auto;
}

.upgrade-log {
  display: grid;
  gap: 0.35rem;
  min-height: 12rem;
  max-height: 24rem;
  overflow: auto;
  padding: 0.75rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: #ffffff;
}

.upgrade-log-empty {
  color: var(--erp-text-muted);
  font-size: 0.88rem;
}

.upgrade-log-line {
  display: grid;
  grid-template-columns: 2.3rem minmax(0, 1fr);
  gap: 0.55rem;
  align-items: start;
  padding: 0.52rem 0.6rem;
  border: 1px solid var(--erp-line);
  border-radius: 7px;
  background: var(--erp-surface-muted);
}

.upgrade-log-line span {
  color: var(--erp-text-muted);
  font-size: 0.72rem;
  font-weight: 850;
}

.upgrade-log-line p {
  margin: 0;
  color: var(--erp-text);
  font-family: var(--erp-font-sans);
  font-size: 0.78rem;
  line-height: 1.45;
  overflow-wrap: anywhere;
}

@keyframes upgrade-spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes upgrade-pulse {
  50% {
    transform: scale(1.04);
  }
}

@media (max-width: 1180px) {
  .upgrade-layout {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 980px) {
  .upgrade-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .upgrade-grid,
  .upgrade-progress-head {
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
