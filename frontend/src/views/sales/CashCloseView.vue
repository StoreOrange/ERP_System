<template>
  <section class="page-section cash-close-page">
    <div class="module-hero">
      <div class="module-hero-copy">
        <p class="page-kicker">Comercial</p>
        <h1 class="page-title">Cierre de Caja Diario</h1>
        <p class="panel-text">
          Compara ventas cobradas en efectivo contra arqueo fisico, ingresos y egresos de caja.
        </p>
      </div>
      <div class="module-hero-meta">
        <div class="module-meta-box">
          <span>Fecha</span>
          <strong>{{ closeDate }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Esperado</span>
          <strong>C$ {{ formatMoney(expectedCash) }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Diferencia</span>
          <strong :class="differenceClass">C$ {{ formatMoney(difference) }}</strong>
        </div>
      </div>
    </div>

    <div v-if="alert.message" class="settings-feedback" :class="alert.type === 'success' ? 'settings-feedback-success' : 'settings-feedback-error'">
      <i class="bi" :class="alert.type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-circle-fill'"></i>
      <span>{{ alert.message }}</span>
    </div>

    <div class="cash-close-grid">
      <article class="panel-card cash-close-panel">
        <div class="panel-head">
          <div>
            <span class="products-section-kicker">Arqueo</span>
            <h3>Resumen del dia</h3>
          </div>
          <Tag :severity="resultSeverity" :value="resultLabel" />
        </div>

        <div class="product-form-grid">
          <label class="field-group">
            <span>Fecha de cierre</span>
            <input v-model="closeDate" class="form-control" type="date" @change="loadSummary" />
          </label>
          <label class="field-group">
            <span>Bodega</span>
            <select v-model="bodegaId" class="form-control" @change="loadSummary">
              <option :value="null">Todas</option>
              <option v-for="bodega in bodegas" :key="bodega.id" :value="bodega.id">
                {{ bodega.name }}
              </option>
            </select>
          </label>
          <label class="field-group">
            <span>Efectivo fisico C$</span>
            <input v-model.number="cashCounted" class="form-control" type="number" min="0" step="0.01" />
          </label>
          <label class="field-group field-span-2">
            <span>Observacion</span>
            <input v-model.trim="observation" class="form-control" placeholder="Nota del cierre, turno o responsable" />
          </label>
        </div>

        <div class="cash-close-kpis">
          <div><span>Facturas</span><strong>{{ summary.invoice_count || 0 }}</strong></div>
          <div><span>Total ventas</span><strong>C$ {{ formatMoney(summary.total_ventas_cs) }}</strong></div>
          <div><span>Efectivo ventas</span><strong>C$ {{ formatMoney(summary.efectivo_ventas_cs) }}</strong></div>
          <div><span>Tarjeta</span><strong>C$ {{ formatMoney(summary.tarjeta_ventas_cs) }}</strong></div>
          <div><span>Transferencias</span><strong>C$ {{ formatMoney(summary.transferencia_ventas_cs) }}</strong></div>
          <div><span>Otros pagos</span><strong>C$ {{ formatMoney(summary.otros_pagos_cs) }}</strong></div>
        </div>

        <div class="cash-close-totals">
          <div><span>Ingresos caja</span><strong>C$ {{ formatMoney(incomeTotal) }}</strong></div>
          <div><span>Egresos caja</span><strong>C$ {{ formatMoney(expenseTotal) }}</strong></div>
          <div><span>Efectivo esperado</span><strong>C$ {{ formatMoney(expectedCash) }}</strong></div>
          <div><span>Efectivo fisico</span><strong>C$ {{ formatMoney(cashCounted) }}</strong></div>
        </div>

        <div class="product-form-actions">
          <Button type="button" severity="secondary" variant="outlined" icon="bi bi-arrow-clockwise" label="Recalcular" @click="loadSummary" />
          <Button type="button" icon="bi bi-check2-circle" :disabled="saving || summary.has_closed" :label="summary.has_closed ? 'Cierre ya registrado' : saving ? 'Cerrando...' : 'Cerrar caja'" @click="submitClose" />
        </div>
      </article>

      <article class="panel-card cash-close-panel">
        <div class="panel-head">
          <div>
            <span class="products-section-kicker">Movimientos manuales</span>
            <h3>Ingresos y egresos de caja</h3>
          </div>
        </div>

        <div class="cash-movement-form">
          <select v-model="movementForm.tipo" class="form-control">
            <option value="INGRESO">Ingreso</option>
            <option value="EGRESO">Egreso</option>
          </select>
          <input v-model.trim="movementForm.concepto" class="form-control" placeholder="Concepto" />
          <input v-model.number="movementForm.monto_cs" class="form-control" type="number" min="0.01" step="0.01" placeholder="Monto C$" />
          <Button type="button" icon="bi bi-plus-lg" label="Agregar" @click="addMovement" />
        </div>

        <div class="cash-movement-list">
          <article v-for="movement in movements" :key="movement.id" class="cash-movement-row">
            <div>
              <strong>{{ movement.concepto }}</strong>
              <span>{{ movement.tipo }}</span>
            </div>
            <b :class="movement.tipo === 'INGRESO' ? 'positive' : 'negative'">
              {{ movement.tipo === "INGRESO" ? "+" : "-" }} C$ {{ formatMoney(movement.monto_cs) }}
            </b>
            <Button type="button" severity="danger" variant="text" rounded icon="bi bi-trash3" @click="removeMovement(movement.id)" />
          </article>
          <div v-if="!movements.length" class="empty-state">No hay ingresos o egresos manuales.</div>
        </div>
      </article>
    </div>

    <article v-if="lastClose" class="panel-card cash-close-receipt">
      <div class="panel-head">
        <div>
          <span class="products-section-kicker">Comprobante POS</span>
          <h3>{{ lastClose.cierre_numero }}</h3>
        </div>
        <Button type="button" icon="bi bi-printer" label="Imprimir cierre" @click="printClose" />
      </div>
      <div class="cash-receipt-print">
        <h3>Cierre de caja</h3>
        <p>{{ lastClose.cierre_numero }} · {{ lastClose.fecha }}</p>
        <hr />
        <p>Total ventas: C$ {{ formatMoney(lastClose.total_ventas_cs) }}</p>
        <p>Efectivo ventas: C$ {{ formatMoney(lastClose.efectivo_ventas_cs) }}</p>
        <p>Ingresos: C$ {{ formatMoney(lastClose.ingresos_caja_cs) }}</p>
        <p>Egresos: C$ {{ formatMoney(lastClose.egresos_caja_cs) }}</p>
        <p>Esperado: C$ {{ formatMoney(lastClose.efectivo_esperado_cs) }}</p>
        <p>Fisico: C$ {{ formatMoney(lastClose.efectivo_fisico_cs) }}</p>
        <h4>{{ lastClose.resultado }} · C$ {{ formatMoney(lastClose.diferencia_cs) }}</h4>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import Button from "primevue/button";
import Tag from "primevue/tag";

import { fetchInventoryCatalogs } from "../../services/inventory";
import { createCashClose, fetchCashCloseSummary } from "../../services/sales";
import { readStoredUser } from "../../services/auth";

const currentUser = readStoredUser();
const closeDate = ref(new Date().toISOString().slice(0, 10));
const bodegaId = ref(null);
const cashCounted = ref(0);
const observation = ref("");
const saving = ref(false);
const summary = ref({});
const bodegas = ref([]);
const movements = ref([]);
const lastClose = ref(null);
const alert = reactive({ type: "", message: "" });
const movementForm = reactive({ tipo: "INGRESO", concepto: "", monto_cs: null });

const incomeTotal = computed(() =>
  movements.value.filter((item) => item.tipo === "INGRESO").reduce((total, item) => total + Number(item.monto_cs || 0), 0),
);
const expenseTotal = computed(() =>
  movements.value.filter((item) => item.tipo === "EGRESO").reduce((total, item) => total + Number(item.monto_cs || 0), 0),
);
const expectedCash = computed(() => Number(summary.value.efectivo_ventas_cs || 0) + incomeTotal.value - expenseTotal.value);
const difference = computed(() => Number(cashCounted.value || 0) - expectedCash.value);
const resultLabel = computed(() => {
  if (difference.value > 0.009) return "Sobrante";
  if (difference.value < -0.009) return "Faltante";
  return "Cuadrado";
});
const resultSeverity = computed(() => {
  if (difference.value > 0.009) return "info";
  if (difference.value < -0.009) return "danger";
  return "success";
});
const differenceClass = computed(() => ({
  positive: difference.value > 0.009,
  negative: difference.value < -0.009,
}));

function formatMoney(value) {
  return new Intl.NumberFormat("es-NI", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(value || 0));
}

function showAlert(type, message) {
  alert.type = type;
  alert.message = message;
  window.setTimeout(() => {
    if (alert.message === message) alert.message = "";
  }, 3500);
}

function addMovement() {
  const amount = Number(movementForm.monto_cs || 0);
  if (!movementForm.concepto || amount <= 0) {
    showAlert("error", "Ingresa concepto y monto valido.");
    return;
  }
  movements.value.push({
    id: `${Date.now()}-${Math.random()}`,
    tipo: movementForm.tipo,
    concepto: movementForm.concepto,
    monto_cs: amount,
  });
  movementForm.concepto = "";
  movementForm.monto_cs = null;
}

function removeMovement(id) {
  movements.value = movements.value.filter((item) => item.id !== id);
}

async function loadSummary() {
  try {
    summary.value = await fetchCashCloseSummary(closeDate.value, bodegaId.value);
    if (!cashCounted.value) {
      cashCounted.value = Number(summary.value.efectivo_ventas_cs || 0);
    }
  } catch (error) {
    showAlert("error", error.message || "No se pudo cargar el resumen de caja.");
  }
}

async function submitClose() {
  saving.value = true;
  try {
    const close = await createCashClose({
      fecha: closeDate.value,
      bodega_id: bodegaId.value ? Number(bodegaId.value) : null,
      efectivo_fisico_cs: Number(cashCounted.value || 0),
      observacion: observation.value,
      usuario_registro: currentUser?.email || currentUser?.full_name || "sistema",
      movements: movements.value.map((item) => ({
        tipo: item.tipo,
        concepto: item.concepto,
        monto_cs: Number(item.monto_cs || 0),
      })),
    });
    lastClose.value = close;
    showAlert("success", `${close.cierre_numero} registrado correctamente.`);
    await loadSummary();
  } catch (error) {
    showAlert("error", error.message || "No se pudo cerrar caja.");
  } finally {
    saving.value = false;
  }
}

function printClose() {
  document.body.classList.add("printing-cash-close");
  window.print();
  window.setTimeout(() => document.body.classList.remove("printing-cash-close"), 500);
}

onMounted(async () => {
  try {
    const catalogs = await fetchInventoryCatalogs();
    bodegas.value = catalogs.bodegas || [];
  } catch {
    bodegas.value = [];
  }
  await loadSummary();
});
</script>

<style scoped>
.cash-close-page,
.cash-close-panel {
  display: grid;
  gap: 1rem;
}

.cash-close-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(22rem, 0.85fr);
  gap: 1rem;
}

.cash-close-kpis,
.cash-close-totals {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.65rem;
}

.cash-close-kpis div,
.cash-close-totals div,
.cash-movement-row {
  padding: 0.75rem;
  border: 1px solid var(--erp-line);
  border-radius: 8px;
  background: var(--erp-surface-muted);
}

.cash-close-kpis span,
.cash-close-totals span,
.cash-movement-row span {
  display: block;
  color: var(--erp-text-muted);
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
}

.cash-close-kpis strong,
.cash-close-totals strong {
  display: block;
  margin-top: 0.25rem;
}

.cash-movement-form {
  display: grid;
  grid-template-columns: 8rem minmax(0, 1fr) 9rem auto;
  gap: 0.5rem;
}

.cash-movement-list {
  display: grid;
  gap: 0.5rem;
}

.cash-movement-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  align-items: center;
  gap: 0.5rem;
}

.positive {
  color: var(--erp-success);
}

.negative {
  color: var(--erp-danger);
}

.cash-receipt-print {
  max-width: 22rem;
  padding: 1rem;
  border: 1px dashed var(--erp-line-strong);
  background: #fff;
  color: #111;
}

@media print {
  body.printing-cash-close * {
    visibility: hidden !important;
  }

  body.printing-cash-close .cash-receipt-print,
  body.printing-cash-close .cash-receipt-print * {
    visibility: visible !important;
  }

  body.printing-cash-close .cash-receipt-print {
    position: fixed;
    top: 0;
    left: 0;
    width: 80mm;
    border: 0;
  }
}

@media (max-width: 980px) {
  .cash-close-grid,
  .cash-close-kpis,
  .cash-close-totals,
  .cash-movement-form {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
