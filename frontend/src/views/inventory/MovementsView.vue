<template>
  <section class="page-section movements-page">
    <header class="module-hero">
      <div class="module-hero-copy">
        <p class="page-kicker">Inventario</p>
        <h1 class="page-title">Ingresos y egresos</h1>
        <p class="panel-text">
          Registra entradas, salidas y traslados en una sola vista operativa, con
          historial inmediato y control por bodega.
        </p>
      </div>
      <div class="module-hero-meta">
        <div class="module-meta-box">
          <span>Ingresos</span>
          <strong>{{ ingresos.length }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Egresos</span>
          <strong>{{ egresos.length }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Total del dia</span>
          <strong>{{ baseCurrencySymbol }} {{ formatMoney(movementTotalCs) }}</strong>
        </div>
      </div>
    </header>

    <div class="movements-modebar">
      <button type="button" class="movements-modechip" :class="{ active: mode === 'ingreso' }" @click="switchMode('ingreso')">
        <i class="bi bi-box-arrow-in-down"></i>
        <span>Ingreso</span>
      </button>
      <button type="button" class="movements-modechip" :class="{ active: mode === 'egreso' }" @click="switchMode('egreso')">
        <i class="bi bi-box-arrow-up-right"></i>
        <span>Egreso</span>
      </button>
      <Tag severity="info" :value="`Bodegas: ${catalogs.bodegas.length}`" rounded />
      <Tag severity="contrast" :value="`Proveedores: ${catalogs.proveedores.length}`" rounded />
    </div>

    <div class="movements-layout">
      <section class="panel-card movement-entry-card">
        <div class="movement-card-head">
          <div>
            <span class="products-section-kicker">Registro operativo</span>
            <h3>{{ mode === "ingreso" ? "Nuevo ingreso" : "Nuevo egreso" }}</h3>
            <p>{{ modeCopy }}</p>
          </div>
          <Tag :severity="mode === 'ingreso' ? 'success' : 'warn'" :value="mode === 'ingreso' ? 'Entrada' : 'Salida'" />
        </div>

        <form class="movement-form" @submit.prevent="submitMovement">
          <div class="movement-form-grid">
            <label class="field-group">
              <span>{{ mode === "ingreso" ? "Tipo de ingreso" : "Tipo de egreso" }}</span>
              <Select
                v-model="form.tipo_id"
                :options="movementTypeOptions"
                option-label="nombre"
                option-value="id"
                placeholder="Seleccionar"
                filter
                :filter-fields="['nombre']"
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
              <small class="movement-money-hint">1 USD = C$ {{ formatMoney(exchangeRate) }}</small>
            </label>

            <label v-if="mode === 'ingreso'" class="field-group field-span-2">
              <span>Proveedor</span>
              <div class="movement-provider-stack">
                <div class="movement-provider-row">
                  <Select
                    v-model="form.proveedor_id"
                    :options="catalogs.proveedores"
                    option-label="nombre"
                    option-value="id"
                    placeholder="Seleccionar"
                    filter
                    :filter-fields="['nombre', 'tipo']"
                    show-clear
                  />
                  <Button
                    type="button"
                    severity="secondary"
                    variant="outlined"
                    icon="bi bi-plus-lg"
                    label="Proveedor"
                    @click="showQuickProvider = !showQuickProvider"
                  />
                </div>
                <div v-if="showQuickProvider" class="movement-provider-quick">
                  <div class="movement-provider-quick-grid">
                    <label class="field-group">
                      <span>Nombre</span>
                      <input v-model="quickProvider.nombre" class="form-control" placeholder="Nombre del proveedor" />
                    </label>
                    <label class="field-group">
                      <span>Tipo</span>
                      <input v-model="quickProvider.tipo" class="form-control" placeholder="Local / Importacion" />
                    </label>
                  </div>
                  <div class="movement-provider-actions">
                    <label class="products-checkbox products-checkbox-compact">
                      <input v-model="quickProvider.activo" type="checkbox" />
                      <span>Activo</span>
                    </label>
                    <Button
                      type="button"
                      :loading="savingQuickProvider"
                      icon="bi bi-save2"
                      label="Guardar proveedor"
                      @click="submitQuickProvider"
                    />
                  </div>
                </div>
              </div>
            </label>

            <label v-if="showDestinationBodega" class="field-group field-span-2">
              <span>Bodega destino</span>
              <Select
                v-model="form.bodega_destino_id"
                :options="destinationBodegas"
                option-label="name"
                option-value="id"
                placeholder="Seleccionar"
                filter
                :filter-fields="['name', 'code']"
              />
            </label>

            <label class="field-group field-span-2">
              <span>Observacion</span>
              <textarea
                v-model="form.observacion"
                class="form-control movement-notes"
                rows="2"
                placeholder="Detalle operativo del movimiento"
              ></textarea>
            </label>
          </div>

          <div class="movement-product-head">
            <div>
              <span class="products-section-kicker">Detalle</span>
              <h4>Productos del movimiento</h4>
            </div>
          </div>

          <div class="movement-product-search">
            <div class="movement-search-box">
              <InputText
                v-model="searchQuery"
                class="search-input"
                type="search"
                placeholder="Buscar por codigo, barra o descripcion"
                @keydown.down.prevent="moveSearchSelection(1)"
                @keydown.up.prevent="moveSearchSelection(-1)"
                @keydown.enter.prevent="handleSearchEnter"
              />
            </div>

            <div class="movement-search-results" v-if="searchQuery.trim().length >= 2">
              <div v-if="searchingProducts" class="empty-state">Buscando productos...</div>
              <div v-else-if="searchResults.length === 0" class="empty-state">Sin resultados para esta busqueda.</div>
              <button
                v-for="(item, index) in searchResults"
                :key="item.id"
                type="button"
                class="movement-result-item"
                :class="{ active: searchActiveIndex === index }"
                :ref="(el) => setSearchResultButton(el, index)"
                @click="selectProduct(item)"
              >
                <div>
                  <strong>{{ item.descripcion }}</strong>
                  <span>{{ item.cod_producto }}<template v-if="item.codigo_barra"> · {{ item.codigo_barra }}</template></span>
                </div>
                <Tag severity="contrast" :value="`Stock: ${formatQty(item.existencia)}`" rounded />
              </button>
            </div>
          </div>

          <div v-if="draft.product_id" class="movement-draft-row">
            <div class="movement-draft-main">
              <strong>{{ draft.descripcion }}</strong>
              <span>{{ draft.cod_producto }} · Disponible {{ formatQty(draft.existencia) }}</span>
            </div>
            <div class="movement-draft-fields">
              <label class="field-group">
                <span>Cantidad</span>
                <InputNumber
                  v-model="draft.cantidad"
                  :min="0"
                  :min-fraction-digits="2"
                  :max-fraction-digits="2"
                  input-class="erp-number-input"
                />
              </label>
              <label class="field-group">
                <span>{{ mode === "ingreso" ? `Costo (${draftCurrencyLabel})` : `Costo ref. (${draftCurrencyLabel})` }}</span>
                <InputNumber
                  v-model="draft.costo_unitario"
                  :min="0"
                  :min-fraction-digits="2"
                  :max-fraction-digits="2"
                  input-class="erp-number-input"
                />
                <small v-if="draftEquivalentText" class="movement-money-hint">{{ draftEquivalentText }}</small>
              </label>
              <Button type="button" icon="bi bi-plus-lg" label="Agregar" @click="appendDraftItem" />
            </div>
          </div>

          <div class="movement-items-table">
            <DataTable :value="items" class="movements-table" responsive-layout="scroll" size="small">
              <Column header="Producto">
                <template #body="{ data }">
                  <div class="products-main-cell">
                    <strong>{{ data.descripcion }}</strong>
                    <small>{{ data.cod_producto }}</small>
                  </div>
                </template>
              </Column>
              <Column header="Cantidad">
                <template #body="{ data }">{{ formatQty(data.cantidad) }}</template>
              </Column>
              <Column header="Costo">
                <template #body="{ data }">
                  <div class="movement-money-cell">
                    <strong>{{ selectedCurrencySymbol }} {{ formatMoney(data.costo_unitario) }}</strong>
                    <small v-if="itemEquivalentLabel(data, 'unit')">{{ itemEquivalentLabel(data, "unit") }}</small>
                  </div>
                </template>
              </Column>
              <Column header="Subtotal">
                <template #body="{ data }">
                  <div class="movement-money-cell">
                    <strong>{{ selectedCurrencySymbol }} {{ formatMoney(itemSubtotal(data)) }}</strong>
                    <small v-if="itemEquivalentLabel(data, 'subtotal')">{{ itemEquivalentLabel(data, "subtotal") }}</small>
                  </div>
                </template>
              </Column>
              <Column header="Acciones">
                <template #body="{ index }">
                  <Button
                    type="button"
                    icon="bi bi-trash3"
                    severity="danger"
                    variant="text"
                    rounded
                    @click="removeItem(index)"
                  />
                </template>
              </Column>
              <template #empty>
                <div class="empty-state">Aun no hay productos agregados.</div>
              </template>
            </DataTable>
          </div>

          <div class="movement-totals">
            <div class="movement-total-box">
              <span>Total {{ selectedCurrencyCode }}</span>
              <strong>{{ selectedCurrencySymbol }} {{ formatMoney(totalInSelectedCurrency) }}</strong>
            </div>
            <div class="movement-total-box">
              <span>Equiv. C$</span>
              <strong>{{ baseCurrencySymbol }} {{ formatMoney(totalCs) }}</strong>
            </div>
            <div class="movement-total-box">
              <span>Equiv. USD</span>
              <strong>US$ {{ formatMoney(totalUsd) }}</strong>
            </div>
          </div>

          <p v-if="formError" class="auth-error">{{ formError }}</p>
          <p v-if="successMessage" class="settings-feedback settings-feedback-success">
            <i class="bi bi-check-circle-fill"></i>
            <span>{{ successMessage }}</span>
          </p>

          <div class="movement-form-actions">
            <Button type="button" severity="secondary" variant="outlined" @click="resetMovementForm">
              Limpiar
            </Button>
            <Button :loading="submitting" type="submit">
              {{ submitting ? "Guardando..." : mode === "ingreso" ? "Registrar ingreso" : "Registrar egreso" }}
            </Button>
          </div>
        </form>
      </section>

      <section class="panel-card movement-history-card">
        <div class="movement-card-head">
          <div>
            <span class="products-section-kicker">Historico</span>
            <h3>Movimientos registrados</h3>
            <p>Vista unificada de entradas y salidas, con referencias de tipo, bodega e importe.</p>
          </div>
        </div>

        <div class="movements-filterbar">
          <button type="button" class="movements-filterchip" :class="{ active: historyFilter === 'all' }" @click="historyFilter = 'all'">Todos</button>
          <button type="button" class="movements-filterchip" :class="{ active: historyFilter === 'INGRESO' }" @click="historyFilter = 'INGRESO'">Ingresos</button>
          <button type="button" class="movements-filterchip" :class="{ active: historyFilter === 'EGRESO' }" @click="historyFilter = 'EGRESO'">Egresos</button>
        </div>

        <DataTable :value="filteredHistory" class="movements-table movement-history-table" paginator :rows="10" responsive-layout="scroll" size="small">
          <Column header="Doc.">
            <template #body="{ data }">{{ data.documento }}</template>
          </Column>
          <Column header="Fecha">
            <template #body="{ data }">{{ data.fecha }}</template>
          </Column>
          <Column header="Tipo">
            <template #body="{ data }">
              <Tag :severity="data.kind === 'INGRESO' ? 'success' : 'warn'" :value="data.kind" rounded />
            </template>
          </Column>
          <Column header="Motivo">
            <template #body="{ data }">{{ data.tipo_nombre }}</template>
          </Column>
          <Column header="Bodega">
            <template #body="{ data }">{{ data.bodega_nombre }}</template>
          </Column>
          <Column header="Detalle">
            <template #body="{ data }">
              <div class="movement-history-detail">
                <strong>{{ data.items_count }} items</strong>
                <span>{{ data.items_preview }}</span>
              </div>
            </template>
          </Column>
          <Column header="Total">
            <template #body="{ data }">{{ baseCurrencySymbol }} {{ formatMoney(data.total_cs) }}</template>
          </Column>
          <template #empty>
            <div class="empty-state">No hay movimientos para el filtro actual.</div>
          </template>
        </DataTable>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue";
import Button from "primevue/button";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import Tag from "primevue/tag";

import { readStoredUser } from "../../services/auth";
import { readStoredBusinessSettings } from "../../services/settings";
import {
  createProveedor,
  createEgreso,
  createIngreso,
  fetchEgresos,
  fetchIngresos,
  fetchInventoryCatalogs,
  fetchProducts,
  searchInventoryProducts,
} from "../../services/inventory";

const currentUser = readStoredUser();
const mode = ref("ingreso");
const historyFilter = ref("all");
const submitting = ref(false);
const searchingProducts = ref(false);
const formError = ref("");
const successMessage = ref("");
const savingQuickProvider = ref(false);
const showQuickProvider = ref(false);
const searchQuery = ref("");
const searchResults = ref([]);
const searchActiveIndex = ref(-1);
const searchResultButtons = ref([]);
const ingresos = ref([]);
const egresos = ref([]);
const products = ref([]);
const searchTimeout = ref(null);
const catalogs = reactive({
  bodegas: [],
  proveedores: [],
  ingreso_tipos: [],
  egreso_tipos: [],
});
const form = reactive(getEmptyMovementForm());
const draft = reactive(getEmptyDraft());
const items = ref([]);
const quickProvider = reactive({
  nombre: "",
  tipo: "",
  activo: true,
});
const DRAFT_STORAGE_KEY = "erp_inventory_movement_draft_v1";
const businessSettings = readStoredBusinessSettings() || {};

const baseCurrencySymbol = "C$";
const selectedCurrencyCode = computed(() => (form.moneda === "USD" ? "USD" : "CS"));
const selectedCurrencySymbol = computed(() => (form.moneda === "USD" ? "US$" : "C$"));
const exchangeRate = computed(() => Number(form.tasa_cambio || 0));
const inventoryCostCurrency = computed(() => {
  if (businessSettings?.inventory_cs_only) return "CS";
  return (businessSettings?.pricing_currency || "CS").toUpperCase() === "USD" ? "USD" : "CS";
});
const movementTypeOptions = computed(() => (mode.value === "ingreso" ? catalogs.ingreso_tipos : catalogs.egreso_tipos));
const selectedIngresoType = computed(() => catalogs.ingreso_tipos.find((item) => item.id === form.tipo_id) || null);
const selectedEgresoType = computed(() => catalogs.egreso_tipos.find((item) => item.id === form.tipo_id) || null);
const requiresProvider = computed(() => mode.value === "ingreso" && Boolean(selectedIngresoType.value?.requiere_proveedor));
const showDestinationBodega = computed(
  () =>
    mode.value === "egreso" &&
    /traslado/i.test(selectedEgresoType.value?.nombre || ""),
);
const destinationBodegas = computed(() => catalogs.bodegas.filter((item) => item.id !== form.bodega_id));
const productMap = computed(() => {
  const map = new Map();
  products.value.forEach((item) => map.set(item.id, item));
  return map;
});
const movementTotalCs = computed(
  () =>
    [...ingresos.value, ...egresos.value].reduce((sum, item) => sum + Number(item.total_cs || 0), 0),
);
const totalInSelectedCurrency = computed(() =>
  items.value.reduce((sum, item) => sum + itemSubtotal(item), 0),
);
const totalCs = computed(() => {
  const total = totalInSelectedCurrency.value;
  if (form.moneda === "CS") return total;
  const rate = Number(form.tasa_cambio || 0);
  return rate > 0 ? total * rate : 0;
});
const totalUsd = computed(() => {
  const total = totalInSelectedCurrency.value;
  if (form.moneda === "USD") return total;
  const rate = Number(form.tasa_cambio || 0);
  return rate > 0 ? total / rate : 0;
});
const modeCopy = computed(() =>
  mode.value === "ingreso"
    ? "Captura compras, inventario inicial, ajustes y entradas por proveedor."
    : "Registra salidas, mermas, inventario fisico o traslados entre bodegas.",
);
const draftCurrencyLabel = computed(() => (form.moneda === "USD" ? "USD" : "C$"));
const draftEquivalentText = computed(() => {
  const value = Number(draft.costo_unitario || 0);
  if (value <= 0) return "";
  const equivalent = form.moneda === "USD"
    ? convertAmount(value, "USD", "CS")
    : convertAmount(value, "CS", "USD");
  if (equivalent <= 0) return "";
  return form.moneda === "USD"
    ? `Equivale a C$ ${formatMoney(equivalent)}`
    : `Equivale a US$ ${formatMoney(equivalent)}`;
});
const combinedHistory = computed(() => {
  const productLookup = productMap.value;
  const ingresoTipos = new Map(catalogs.ingreso_tipos.map((item) => [item.id, item.nombre]));
  const egresoTipos = new Map(catalogs.egreso_tipos.map((item) => [item.id, item.nombre]));
  const bodegas = new Map(catalogs.bodegas.map((item) => [item.id, item.name]));

  const toPreview = (movementItems) =>
    movementItems
      .slice(0, 3)
      .map((item) => productLookup.get(item.producto_id)?.descripcion || `#${item.producto_id}`)
      .join(", ");

  return [
    ...ingresos.value.map((item) => ({
      id: item.id,
      documento: `ING-${item.id}`,
      fecha: item.fecha,
      kind: "INGRESO",
      tipo_nombre: ingresoTipos.get(item.tipo_id) || "Ingreso",
      bodega_nombre: bodegas.get(item.bodega_id) || "-",
      total_cs: Number(item.total_cs || 0),
      items_count: item.items.length,
      items_preview: toPreview(item.items),
    })),
    ...egresos.value.map((item) => ({
      id: item.id,
      documento: `EGR-${item.id}`,
      fecha: item.fecha,
      kind: "EGRESO",
      tipo_nombre: egresoTipos.get(item.tipo_id) || "Egreso",
      bodega_nombre: bodegas.get(item.bodega_id) || "-",
      total_cs: Number(item.total_cs || 0),
      items_count: item.items.length,
      items_preview: toPreview(item.items),
    })),
  ].sort((a, b) => `${b.fecha}-${b.id}`.localeCompare(`${a.fecha}-${a.id}`));
});
const filteredHistory = computed(() =>
  historyFilter.value === "all"
    ? combinedHistory.value
    : combinedHistory.value.filter((item) => item.kind === historyFilter.value),
);

function getEmptyMovementForm() {
  return {
    tipo_id: null,
    bodega_id: null,
    bodega_destino_id: null,
    proveedor_id: null,
    fecha: new Date().toISOString().slice(0, 10),
    moneda: "CS",
    tasa_cambio: null,
    observacion: "",
    usuario_registro: currentUser?.email || "sistema",
  };
}

function getEmptyDraft() {
  return {
    product_id: null,
    cod_producto: "",
    descripcion: "",
    existencia: 0,
    cantidad: 1,
    costo_unitario: 0,
  };
}

function resetDraft() {
  Object.assign(draft, getEmptyDraft());
  searchQuery.value = "";
  searchResults.value = [];
  searchActiveIndex.value = -1;
  searchResultButtons.value = [];
}

function resetQuickProvider() {
  quickProvider.nombre = "";
  quickProvider.tipo = "";
  quickProvider.activo = true;
}

function resetMovementForm() {
  Object.assign(form, getEmptyMovementForm());
  items.value = [];
  formError.value = "";
  successMessage.value = "";
  showQuickProvider.value = false;
  resetQuickProvider();
  resetDraft();
  if (mode.value === "ingreso") {
    const localProvider = catalogs.proveedores.find((item) => /local/i.test(item.nombre || ""));
    if (localProvider) {
      form.proveedor_id = localProvider.id;
    }
  }
}

function switchMode(nextMode) {
  mode.value = nextMode;
  resetMovementForm();
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

function itemSubtotal(item) {
  return Number(item.cantidad || 0) * Number(item.costo_unitario || 0);
}

function convertAmount(amount, fromCurrency, toCurrency) {
  const numericAmount = Number(amount || 0);
  const rate = exchangeRate.value;
  if (numericAmount <= 0) return 0;
  if (fromCurrency === toCurrency) return numericAmount;
  if (rate <= 0) return 0;
  if (fromCurrency === "USD" && toCurrency === "CS") return numericAmount * rate;
  if (fromCurrency === "CS" && toCurrency === "USD") return numericAmount / rate;
  return 0;
}

function itemEquivalentLabel(item, kind = "subtotal") {
  const amount = kind === "unit" ? Number(item.costo_unitario || 0) : itemSubtotal(item);
  if (amount <= 0) return "";
  const equivalent = form.moneda === "USD"
    ? convertAmount(amount, "USD", "CS")
    : convertAmount(amount, "CS", "USD");
  if (equivalent <= 0) return "";
  return form.moneda === "USD"
    ? `C$ ${formatMoney(equivalent)}`
    : `US$ ${formatMoney(equivalent)}`;
}

function normalizeCostForForm(rawCost) {
  const cost = Number(rawCost || 0);
  if (cost <= 0) return 0;
  if (inventoryCostCurrency.value === form.moneda) return cost;
  return convertAmount(cost, inventoryCostCurrency.value, form.moneda);
}

function selectProduct(item) {
  const meta = productMap.value.get(item.id);
  draft.product_id = item.id;
  draft.cod_producto = item.cod_producto || "";
  draft.descripcion = item.descripcion || "";
  draft.existencia = Number(item.existencia || 0);
  draft.cantidad = 1;
  draft.costo_unitario = normalizeCostForForm(meta?.costo_producto || 0);
  searchQuery.value = `${item.cod_producto} - ${item.descripcion}`;
  searchResults.value = [];
  searchActiveIndex.value = -1;
  searchResultButtons.value = [];
}

function setSearchResultButton(element, index) {
  if (element) {
    searchResultButtons.value[index] = element;
  }
}

async function scrollSearchResultIntoView(index) {
  await nextTick();
  searchResultButtons.value[index]?.scrollIntoView({
    block: "nearest",
    behavior: "smooth",
  });
}

function moveSearchSelection(direction) {
  if (!searchResults.value.length) {
    return;
  }

  if (searchActiveIndex.value === -1) {
    searchActiveIndex.value = direction > 0 ? 0 : searchResults.value.length - 1;
  } else {
    searchActiveIndex.value =
      (searchActiveIndex.value + direction + searchResults.value.length) % searchResults.value.length;
  }

  void scrollSearchResultIntoView(searchActiveIndex.value);
}

function handleSearchEnter() {
  if (!searchResults.value.length) {
    return;
  }

  if (searchActiveIndex.value === -1) {
    searchActiveIndex.value = 0;
    return;
  }

  selectProduct(searchResults.value[searchActiveIndex.value]);
}

function appendDraftItem() {
  if (!draft.product_id) {
    formError.value = "Selecciona un producto para agregarlo al movimiento.";
    return;
  }
  if (Number(draft.cantidad || 0) <= 0) {
    formError.value = "La cantidad debe ser mayor que cero.";
    return;
  }
  if (mode.value === "egreso" && Number(draft.existencia || 0) < Number(draft.cantidad || 0)) {
    formError.value = `Stock insuficiente para ${draft.cod_producto}. Disponible: ${formatQty(draft.existencia)}.`;
    return;
  }

  const existing = items.value.find((item) => item.producto_id === draft.product_id);
  if (existing) {
    existing.cantidad = Number(existing.cantidad || 0) + Number(draft.cantidad || 0);
    existing.costo_unitario = Number(draft.costo_unitario || 0);
  } else {
    items.value.push({
      producto_id: draft.product_id,
      cod_producto: draft.cod_producto,
      descripcion: draft.descripcion,
      cantidad: Number(draft.cantidad || 0),
      costo_unitario: Number(draft.costo_unitario || 0),
    });
  }
  formError.value = "";
  resetDraft();
}

function removeItem(index) {
  items.value.splice(index, 1);
}

function saveMovementDraft() {
  try {
    const payload = {
      mode: mode.value,
      form: {
        tipo_id: form.tipo_id,
        bodega_id: form.bodega_id,
        bodega_destino_id: form.bodega_destino_id,
        proveedor_id: form.proveedor_id,
        fecha: form.fecha,
        moneda: form.moneda,
        tasa_cambio: form.tasa_cambio,
        observacion: form.observacion,
      },
      items: items.value,
    };
    localStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // ignore local draft errors
  }
}

function restoreMovementDraft() {
  try {
    const raw = localStorage.getItem(DRAFT_STORAGE_KEY);
    if (!raw) return;
    const draftPayload = JSON.parse(raw);
    if (!draftPayload || draftPayload.mode !== mode.value) return;
    Object.assign(form, {
      ...getEmptyMovementForm(),
      ...draftPayload.form,
      usuario_registro: currentUser?.email || "sistema",
    });
    items.value = Array.isArray(draftPayload.items) ? [...draftPayload.items] : [];
  } catch {
    // ignore malformed draft
  }
}

async function submitQuickProvider() {
  formError.value = "";
  if (!(quickProvider.nombre || "").trim()) {
    formError.value = "El nombre del proveedor es requerido.";
    return;
  }
  savingQuickProvider.value = true;
  try {
    const payload = await createProveedor({
      nombre: quickProvider.nombre.trim(),
      tipo: (quickProvider.tipo || "").trim() || null,
      activo: Boolean(quickProvider.activo),
    });
    catalogs.proveedores = [...catalogs.proveedores, payload].sort((a, b) => (a.nombre || "").localeCompare(b.nombre || ""));
    form.proveedor_id = payload.id;
    showQuickProvider.value = false;
    resetQuickProvider();
    successMessage.value = "Proveedor creado y seleccionado.";
  } catch (err) {
    formError.value = err.message || "No se pudo guardar el proveedor.";
  } finally {
    savingQuickProvider.value = false;
  }
}

async function loadMovementData() {
  const [catalogData, productData, ingresosData, egresosData] = await Promise.all([
    fetchInventoryCatalogs(),
    fetchProducts("", true),
    fetchIngresos(),
    fetchEgresos(),
  ]);
  catalogs.bodegas = catalogData.bodegas || [];
  catalogs.proveedores = catalogData.proveedores || [];
  catalogs.ingreso_tipos = catalogData.ingreso_tipos || [];
  catalogs.egreso_tipos = catalogData.egreso_tipos || [];
  products.value = productData || [];
  ingresos.value = ingresosData || [];
  egresos.value = egresosData || [];
  resetMovementForm();
  restoreMovementDraft();
}

async function submitMovement() {
  formError.value = "";
  successMessage.value = "";

  if (!form.tipo_id) {
    formError.value = `Selecciona un ${mode.value === "ingreso" ? "tipo de ingreso" : "tipo de egreso"}.`;
    return;
  }
  if (!form.bodega_id) {
    formError.value = "Selecciona la bodega del movimiento.";
    return;
  }
  if (requiresProvider.value && !form.proveedor_id) {
    formError.value = "Este tipo de ingreso requiere proveedor.";
    return;
  }
  if (showDestinationBodega.value && !form.bodega_destino_id) {
    formError.value = "Selecciona la bodega destino para este traslado.";
    return;
  }
  if (form.moneda === "USD" && Number(form.tasa_cambio || 0) <= 0) {
    formError.value = "La tasa de cambio es requerida cuando la moneda es USD.";
    return;
  }
  if (!items.value.length) {
    formError.value = "Debes agregar al menos un producto al movimiento.";
    return;
  }

  submitting.value = true;
  try {
    const payload = {
      tipo_id: form.tipo_id,
      bodega_id: form.bodega_id,
      fecha: form.fecha,
      moneda: form.moneda,
      tasa_cambio: Number(form.tasa_cambio || 0) > 0 ? Number(form.tasa_cambio || 0) : null,
      observacion: form.observacion || null,
      usuario_registro: form.usuario_registro,
      items: items.value.map((item) => ({
        producto_id: item.producto_id,
        cantidad: Number(item.cantidad || 0),
        costo_unitario: Number(item.costo_unitario || 0),
      })),
      ...(mode.value === "ingreso"
        ? {
            proveedor_id: form.proveedor_id,
          }
        : {
            bodega_destino_id: showDestinationBodega.value ? form.bodega_destino_id : null,
          }),
    };

    if (mode.value === "ingreso") {
      await createIngreso(payload);
    } else {
      await createEgreso(payload);
    }

    await loadMovementData();
    successMessage.value =
      mode.value === "ingreso"
        ? "Ingreso de inventario registrado correctamente."
        : "Egreso de inventario registrado correctamente.";
  } catch (err) {
    formError.value = err.message || "No se pudo registrar el movimiento.";
  } finally {
    submitting.value = false;
  }
}

watch(
  () => form.moneda,
  (nextCurrency, previousCurrency) => {
    if (!previousCurrency || previousCurrency === nextCurrency) {
      return;
    }
    if (Number(form.tasa_cambio || 0) <= 0) {
      return;
    }
    items.value = items.value.map((item) => ({
      ...item,
      costo_unitario: convertAmount(item.costo_unitario, previousCurrency, nextCurrency),
    }));
    if (draft.product_id) {
      draft.costo_unitario = convertAmount(draft.costo_unitario, previousCurrency, nextCurrency);
    }
  },
);

watch(
  () => [searchQuery.value, form.bodega_id, mode.value],
  () => {
    if (searchTimeout.value) {
      clearTimeout(searchTimeout.value);
    }
    const query = searchQuery.value.trim();
    if (draft.product_id && query === `${draft.cod_producto} - ${draft.descripcion}`) {
      return;
    }
    if (query.length < 2) {
      searchResults.value = [];
      searchActiveIndex.value = -1;
      searchResultButtons.value = [];
      if (!query) {
        Object.assign(draft, getEmptyDraft());
      }
      return;
    }
    searchTimeout.value = setTimeout(async () => {
      searchingProducts.value = true;
      try {
        const response = await searchInventoryProducts(query, form.bodega_id || null, 1);
        searchResults.value = response.items || [];
        searchActiveIndex.value = searchResults.value.length ? 0 : -1;
        searchResultButtons.value = [];
        if (searchResults.value.length) {
          void scrollSearchResultIntoView(0);
        }
      } catch {
        searchResults.value = [];
        searchActiveIndex.value = -1;
        searchResultButtons.value = [];
      } finally {
        searchingProducts.value = false;
      }
    }, 220);
  },
);

watch(
  () => [mode.value, form.tipo_id],
  () => {
    if (!showDestinationBodega.value) {
      form.bodega_destino_id = null;
    }
    if (mode.value === "ingreso" && !form.proveedor_id) {
      const localProvider = catalogs.proveedores.find((item) => /local/i.test(item.nombre || ""));
      if (localProvider) {
        form.proveedor_id = localProvider.id;
      }
    }
  },
);

onMounted(async () => {
  try {
    await loadMovementData();
  } catch (err) {
    formError.value = err.message || "No se pudo cargar el modulo de movimientos.";
  }
});

watch(
  () => ({
    mode: mode.value,
    form: {
      tipo_id: form.tipo_id,
      bodega_id: form.bodega_id,
      bodega_destino_id: form.bodega_destino_id,
      proveedor_id: form.proveedor_id,
      fecha: form.fecha,
      moneda: form.moneda,
      tasa_cambio: form.tasa_cambio,
      observacion: form.observacion,
    },
    items: items.value,
  }),
  () => {
    saveMovementDraft();
  },
  { deep: true },
);
</script>
