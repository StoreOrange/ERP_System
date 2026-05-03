<template>
  <section class="page-section production-page">
    <header class="module-hero">
      <div class="module-hero-copy">
        <p class="page-kicker">Inventario</p>
        <h1 class="page-title">Produccion abierta</h1>
        <p class="panel-text">
          Controla la apertura de produccion, descarga de insumos por receta y el ingreso del
          producto final en una sola operacion.
        </p>
      </div>
      <div class="module-hero-meta">
        <div class="module-meta-box">
          <span>Ordenes</span>
          <strong>{{ productions.length }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Abiertas</span>
          <strong>{{ openCount }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Finalizadas</span>
          <strong>{{ completedCount }}</strong>
        </div>
      </div>
    </header>

    <div class="movements-layout">
      <section class="panel-card movement-entry-card">
        <div class="movement-card-head">
          <div>
            <span class="products-section-kicker">Apertura</span>
            <h3>Nueva produccion</h3>
            <p>Selecciona el producto final por receta y deja lista la orden para ejecutar.</p>
          </div>
          <Tag severity="info" value="Produccion" />
        </div>

        <form class="movement-form" @submit.prevent="submitProduction">
          <div class="movement-form-grid">
            <label class="field-group field-span-2">
              <span>Producto final</span>
              <Select
                v-model="form.producto_final_id"
                :options="recipeProducts"
                option-label="descripcion"
                option-value="id"
                placeholder="Seleccionar"
                filter
                :filter-fields="['cod_producto', 'descripcion']"
              />
            </label>

            <label class="field-group">
              <span>Bodega</span>
              <Select
                v-model="form.bodega_id"
                :options="catalogs.bodegas"
                option-label="name"
                option-value="id"
                placeholder="Seleccionar"
                filter
                :filter-fields="['name', 'code']"
              />
            </label>

            <label class="field-group">
              <span>Fecha</span>
              <input v-model="form.fecha" class="form-control" type="date" />
            </label>

            <label class="field-group">
              <span>Moneda</span>
              <select v-model="form.moneda" class="form-control">
                <option value="CS">Cordobas (C$)</option>
                <option value="USD">Dolares (USD)</option>
              </select>
            </label>

            <label class="field-group">
              <span>Tasa de cambio</span>
              <InputNumber
                v-model="form.tasa_cambio"
                :min="0"
                :min-fraction-digits="2"
                :max-fraction-digits="4"
                input-class="erp-number-input"
              />
            </label>

            <label class="field-group">
              <span>Cantidad a producir</span>
              <InputNumber
                v-model="form.cantidad_producida"
                :min="0"
                :min-fraction-digits="2"
                :max-fraction-digits="4"
                input-class="erp-number-input"
              />
            </label>

            <label class="field-group field-span-2">
              <span>Observacion</span>
              <textarea
                v-model="form.observacion"
                class="form-control movement-notes"
                rows="2"
                placeholder="Motivo o contexto de la produccion"
              ></textarea>
            </label>
          </div>

          <p v-if="formError" class="auth-error">{{ formError }}</p>
          <p v-if="successMessage" class="settings-feedback settings-feedback-success">
            <i class="bi bi-check-circle-fill"></i>
            <span>{{ successMessage }}</span>
          </p>

          <div class="movement-form-actions">
            <Button type="button" severity="secondary" variant="outlined" @click="resetForm">
              Limpiar
            </Button>
            <Button :loading="submitting" type="submit">
              {{ submitting ? "Abriendo..." : "Abrir produccion" }}
            </Button>
          </div>
        </form>

        <div v-if="selectedReport" class="production-report">
          <div class="movement-card-head">
            <div>
              <span class="products-section-kicker">Informe</span>
              <h3>Orden #{{ selectedReport.id }}</h3>
              <p>
                {{ selectedReport.producto_final?.cod_producto }} ·
                {{ selectedReport.producto_final?.descripcion }}
              </p>
            </div>
            <Tag :severity="selectedReport.estado === 'FINALIZADA' ? 'success' : 'warn'" :value="selectedReport.estado" />
          </div>

          <div class="movement-totals">
            <div class="movement-total-box">
              <span>Insumos C$</span>
              <strong>C$ {{ formatMoney(selectedReport.total_insumos_cs) }}</strong>
            </div>
            <div class="movement-total-box">
              <span>Produccion C$</span>
              <strong>C$ {{ formatMoney(selectedReport.total_produccion_cs) }}</strong>
            </div>
            <div class="movement-total-box">
              <span>Documentos</span>
              <strong>ING {{ selectedReport.ingreso_id || "-" }} / EGR {{ selectedReport.egreso_id || "-" }}</strong>
            </div>
          </div>

          <DataTable :value="selectedReport.lineas || []" class="movements-table" responsive-layout="scroll" size="small">
            <Column field="tipo_linea" header="Tipo" />
            <Column header="Producto">
              <template #body="{ data }">
                <div class="products-main-cell">
                  <strong>{{ data.producto?.descripcion || `#${data.producto_id}` }}</strong>
                  <small>{{ data.producto?.cod_producto || "" }}</small>
                </div>
              </template>
            </Column>
            <Column header="Cantidad">
              <template #body="{ data }">{{ formatQty(data.cantidad) }}</template>
            </Column>
            <Column header="Costo C$">
              <template #body="{ data }">C$ {{ formatMoney(data.costo_unitario_cs) }}</template>
            </Column>
            <Column header="Subtotal C$">
              <template #body="{ data }">C$ {{ formatMoney(data.subtotal_cs) }}</template>
            </Column>
          </DataTable>
        </div>
      </section>

      <section class="panel-card movement-history-card">
        <div class="movement-card-head">
          <div>
            <span class="products-section-kicker">Historico</span>
            <h3>Producciones registradas</h3>
            <p>Desde aqui ejecutas la orden y revisas el detalle completo del consumo y del ingreso final.</p>
          </div>
        </div>

        <DataTable :value="productions" class="movements-table movement-history-table" paginator :rows="10" responsive-layout="scroll" size="small">
          <Column header="Orden">
            <template #body="{ data }">PRD-{{ data.id }}</template>
          </Column>
          <Column header="Fecha">
            <template #body="{ data }">{{ data.fecha }}</template>
          </Column>
          <Column header="Estado">
            <template #body="{ data }">
              <Tag :severity="data.estado === 'FINALIZADA' ? 'success' : 'warn'" :value="data.estado" rounded />
            </template>
          </Column>
          <Column header="Producto">
            <template #body="{ data }">
              <div class="products-main-cell">
                <strong>{{ data.producto_final?.descripcion || "-" }}</strong>
                <small>{{ data.producto_final?.cod_producto || "" }}</small>
              </div>
            </template>
          </Column>
          <Column header="Cantidad">
            <template #body="{ data }">{{ formatQty(data.cantidad_producida) }}</template>
          </Column>
          <Column header="Total C$">
            <template #body="{ data }">C$ {{ formatMoney(data.total_produccion_cs) }}</template>
          </Column>
          <Column header="Acciones">
            <template #body="{ data }">
              <div class="products-actions-cell">
                <Button type="button" icon="bi bi-eye" severity="secondary" variant="text" rounded @click="viewReport(data.id)" />
                <Button
                  v-if="data.estado === 'ABIERTA'"
                  type="button"
                  icon="bi bi-play-circle"
                  severity="success"
                  variant="text"
                  rounded
                  @click="runProduction(data.id)"
                />
              </div>
            </template>
          </Column>
        </DataTable>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import Button from "primevue/button";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import InputNumber from "primevue/inputnumber";
import Select from "primevue/select";
import Tag from "primevue/tag";

import { readStoredUser } from "../../services/auth";
import {
  executeProduction,
  fetchInventoryCatalogs,
  fetchProductionReport,
  fetchProductions,
  fetchProducts,
  openProduction,
} from "../../services/inventory";

const currentUser = readStoredUser();
const submitting = ref(false);
const formError = ref("");
const successMessage = ref("");
const products = ref([]);
const productions = ref([]);
const selectedReport = ref(null);
const catalogs = reactive({ bodegas: [] });
const form = reactive(getEmptyForm());

const recipeProducts = computed(() =>
  products.value.filter((item) => (item.tipo_producto || "DIRECTO").toUpperCase() === "RECETA"),
);
const openCount = computed(() => productions.value.filter((item) => item.estado === "ABIERTA").length);
const completedCount = computed(() => productions.value.filter((item) => item.estado === "FINALIZADA").length);

function getEmptyForm() {
  return {
    producto_final_id: null,
    bodega_id: null,
    fecha: new Date().toISOString().slice(0, 10),
    cantidad_producida: 1,
    moneda: "CS",
    tasa_cambio: null,
    observacion: "",
    usuario_registro: currentUser?.email || "sistema",
  };
}

function resetForm() {
  Object.assign(form, getEmptyForm());
  formError.value = "";
  successMessage.value = "";
}

function formatMoney(value) {
  return new Intl.NumberFormat("es-NI", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value || 0));
}

function formatQty(value) {
  return Number(value || 0).toFixed(2);
}

async function loadData() {
  const [catalogData, productData, productionData] = await Promise.all([
    fetchInventoryCatalogs(),
    fetchProducts("", true),
    fetchProductions(),
  ]);
  catalogs.bodegas = catalogData.bodegas || [];
  products.value = productData || [];
  productions.value = productionData || [];
}

async function submitProduction() {
  formError.value = "";
  successMessage.value = "";
  submitting.value = true;
  try {
    const opened = await openProduction({
      ...form,
      cantidad_producida: Number(form.cantidad_producida || 0),
      tasa_cambio: Number(form.tasa_cambio || 0) > 0 ? Number(form.tasa_cambio || 0) : null,
    });
    await loadData();
    selectedReport.value = await fetchProductionReport(opened.id);
    successMessage.value = "Produccion abierta correctamente.";
    resetForm();
  } catch (error) {
    formError.value = error.message || "No se pudo abrir la produccion.";
  } finally {
    submitting.value = false;
  }
}

async function runProduction(productionId) {
  formError.value = "";
  successMessage.value = "";
  try {
    await executeProduction(productionId);
    await loadData();
    selectedReport.value = await fetchProductionReport(productionId);
    successMessage.value = "Produccion ejecutada con egreso e ingreso automatico.";
  } catch (error) {
    formError.value = error.message || "No se pudo ejecutar la produccion.";
  }
}

async function viewReport(productionId) {
  formError.value = "";
  try {
    selectedReport.value = await fetchProductionReport(productionId);
  } catch (error) {
    formError.value = error.message || "No se pudo cargar el informe.";
  }
}

onMounted(async () => {
  try {
    await loadData();
  } catch (error) {
    formError.value = error.message || "No se pudo cargar el modulo de produccion.";
  }
});
</script>
