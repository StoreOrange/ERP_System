<template>
  <section class="page-section products-page">
    <header class="products-header">
      <div>
        <p class="page-kicker">Inventario</p>
        <h1 class="page-title">Productos</h1>
        <p class="panel-text">
          Catalogo maestro para inventario, precios y control comercial.
        </p>
      </div>
      <div class="products-header-actions">
        <Button label="Nuevo producto" icon="bi bi-plus-lg" @click="openCreateDialog" />
      </div>
    </header>

    <div class="products-kpi-strip">
      <div class="products-kpi-card products-kpi-card-primary">
        <span>Total</span>
        <strong>{{ products.length }}</strong>
      </div>
      <div class="products-kpi-card">
        <span>Activos</span>
        <strong>{{ activeCount }}</strong>
      </div>
      <div class="products-kpi-card">
        <span>Inactivos</span>
        <strong>{{ inactiveCount }}</strong>
      </div>
      <div class="products-kpi-card">
        <span>Vista</span>
        <strong>{{ showInactive ? "Completa" : "Activos" }}</strong>
      </div>
    </div>

    <div class="products-toolbar">
      <div class="products-toolbar-left">
        <IconField>
          <InputIcon class="bi bi-search" />
          <InputText
            v-model="search"
            class="search-input"
            type="search"
            placeholder="Buscar por codigo, barra o descripcion"
          />
        </IconField>
        <label class="products-checkbox products-checkbox-inline">
          <Checkbox v-model="showInactive" binary />
          <span>Mostrar inactivos</span>
        </label>
      </div>
      <div class="products-toolbar-right">
        <Button
          label="Marcas"
          icon="bi bi-tags"
          severity="secondary"
          variant="outlined"
          @click="openBrandDialog"
        />
        <Button
          label="Subcatalogos"
          icon="bi bi-diagram-3"
          severity="secondary"
          variant="outlined"
          @click="openCatalogDialog"
        />
        <Tag severity="info" :value="`Moneda base: ${currencyLabel}`" rounded />
        <Tag severity="contrast" :value="`${filteredProducts.length} registros`" rounded />
      </div>
    </div>

    <div class="content-grid products-content-grid">
      <Card class="panel-card products-summary-card">
        <template #title>
          <div class="products-table-head">
            <div>
              <span class="products-section-kicker">Estructura</span>
              <h3>Catalogos base</h3>
            </div>
          </div>
        </template>
        <template #content>
          <div class="products-summary-grid">
            <div class="products-summary-item">
              <span>Lineas</span>
              <strong>{{ catalogs.lineas }}</strong>
            </div>
            <div class="products-summary-item">
              <span>Segmentos</span>
              <strong>{{ catalogs.segmentos }}</strong>
            </div>
            <div class="products-summary-item">
              <span>Unidades</span>
              <strong>{{ catalogs.unidades }}</strong>
            </div>
            <div class="products-summary-item">
              <span>Bodegas</span>
              <strong>{{ catalogs.bodegas }}</strong>
            </div>
            <div class="products-summary-item">
              <span>Control</span>
              <strong>Altas, edicion y estado</strong>
            </div>
            <div class="products-summary-item">
              <span>Operacion</span>
              <strong>Inventario y ventas</strong>
            </div>
          </div>
        </template>
      </Card>

      <Card class="panel-card products-table-card">
        <template #title>
          <div class="products-table-head">
            <div>
              <span class="products-section-kicker">Operacion diaria</span>
              <h3>Listado de productos</h3>
            </div>
          </div>
        </template>
        <template #content>
          <div v-if="loading" class="empty-state">Cargando productos...</div>
          <div v-else-if="error" class="empty-state error">{{ error }}</div>
          <DataTable
            v-else
            :value="filteredProducts"
            paginator
            :rows="10"
            responsive-layout="scroll"
            class="products-table"
            size="small"
          >
            <Column header="Producto">
              <template #body="{ data }">
                <div class="products-main-cell">
                  <strong>{{ data.descripcion }}</strong>
                  <small>{{ data.cod_producto }}<template v-if="data.codigo_barra"> · {{ data.codigo_barra }}</template></small>
                </div>
              </template>
            </Column>
            <Column header="Linea">
              <template #body="{ data }">
                {{ data.linea?.linea || "-" }}
              </template>
            </Column>
            <Column header="Segmento">
              <template #body="{ data }">
                {{ data.segmento?.segmento || "-" }}
              </template>
            </Column>
            <Column header="Precio 1">
              <template #body="{ data }">
                {{ currencySymbol }} {{ formatMoney(data.precio_venta1) }}
              </template>
            </Column>
            <Column header="Costo">
              <template #body="{ data }">
                {{ currencySymbol }} {{ formatMoney(data.costo_producto) }}
              </template>
            </Column>
            <Column header="Stock">
              <template #body="{ data }">
                {{ formatQty(data.saldo?.existencia ?? 0) }}
              </template>
            </Column>
            <Column header="Estado">
              <template #body="{ data }">
                <Tag :severity="data.activo ? 'success' : 'contrast'" :value="data.activo ? 'Activo' : 'Inactivo'" />
              </template>
            </Column>
            <Column header="Acciones">
              <template #body="{ data }">
                <div class="products-actions-cell">
                  <Button
                    icon="bi bi-pencil-square"
                    severity="secondary"
                    variant="text"
                    rounded
                    @click="openEditDialog(data)"
                  />
                  <Button
                    :icon="data.activo ? 'bi bi-pause-circle' : 'bi bi-play-circle'"
                    severity="secondary"
                    variant="text"
                    rounded
                    @click="toggleActive(data)"
                  />
                </div>
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <Dialog
      v-model:visible="dialogVisible"
      modal
      :header="editingProductId ? 'Editar producto' : 'Nuevo producto'"
      :style="{ width: 'min(980px, 96vw)' }"
      class="product-dialog"
    >
      <form class="product-form odoo-form-shell" @submit.prevent="submitForm">
        <div class="odoo-form-toolbar">
          <div class="odoo-form-titleblock">
            <span class="odoo-form-kicker">{{ editingProductId ? "Producto existente" : "Nuevo producto" }}</span>
            <div class="odoo-form-titleline">
              <h3>{{ form.descripcion || "Producto sin descripcion" }}</h3>
              <span class="odoo-form-code">{{ form.cod_producto || "-----" }}</span>
            </div>
          </div>

          <div class="odoo-form-switches">
            <label class="odoo-switch">
              <Checkbox v-model="form.activo" binary />
              <span>Activo</span>
            </label>
            <label class="odoo-switch">
              <Checkbox v-model="form.servicio_producto" binary />
              <span>Servicio</span>
            </label>
            <label class="odoo-switch">
              <Checkbox v-model="form.es_por_peso" binary />
              <span>Venta por peso</span>
            </label>
          </div>
        </div>

        <div class="odoo-notebook-tabs" role="tablist" aria-label="Ficha producto">
          <button
            type="button"
            class="odoo-tab"
            :class="{ active: currentFormTab === 'general' }"
            @click="currentFormTab = 'general'"
          >
            Datos del producto
          </button>
          <button
            type="button"
            class="odoo-tab"
            :class="{ active: currentFormTab === 'commercial' }"
            @click="currentFormTab = 'commercial'"
          >
            Costos & Precios
          </button>
        </div>

        <div class="odoo-sheet">
          <div v-if="currentFormTab === 'general'" class="odoo-sheet-section">
            <div class="odoo-field-grid">
              <div class="odoo-field field-span-3">
                <span class="odoo-field-label">Descripcion</span>
                <InputText
                  v-model.trim="form.descripcion"
                  :disabled="saving"
                  maxlength="200"
                  @input="form.descripcion = toUpperValue(form.descripcion)"
                  @focus="selectField"
                />
              </div>

              <div class="odoo-field field-span-1">
                <span class="odoo-field-label">Codigo</span>
                <div class="product-stock-readonly product-code-readonly odoo-compact-readonly">
                  {{ form.cod_producto || "Generando..." }}
                </div>
              </div>

              <div class="odoo-field field-span-2">
                <div class="odoo-field-inlinehead">
                  <span class="odoo-field-label">Codigo de barra</span>
                  <label class="products-checkbox products-checkbox-inline products-checkbox-compact">
                    <Checkbox v-model="form.usa_codigo_barra" binary @change="handleBarcodeToggle" />
                    <span>Usar lector</span>
                  </label>
                </div>
                <InputText
                  v-model.trim="form.codigo_barra"
                  :disabled="!form.usa_codigo_barra"
                  maxlength="120"
                  :placeholder="form.usa_codigo_barra ? 'Escanear o digitar codigo de barra' : 'Active el uso de codigo de barra'"
                  @input="form.codigo_barra = toUpperValue(form.codigo_barra)"
                  @focus="selectField"
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Linea</span>
                <Select
                  v-model="form.linea_id"
                  :options="catalogOptions.lineas"
                  option-label="linea"
                  option-value="id"
                  placeholder="Seleccionar"
                  filter
                  :filter-fields="['linea', 'cod_linea']"
                  show-clear
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Segmento</span>
                <Select
                  v-model="form.segmento_id"
                  :options="catalogOptions.segmentos"
                  option-label="segmento"
                  option-value="id"
                  placeholder="Seleccionar"
                  filter
                  :filter-fields="['segmento']"
                  show-clear
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Unidad</span>
                <Select
                  v-model="form.unidad_medida_id"
                  :options="catalogOptions.unidades"
                  option-label="nombre"
                  option-value="id"
                  placeholder="Seleccionar"
                  filter
                  :filter-fields="['nombre', 'codigo', 'abreviatura']"
                  show-clear
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Marca</span>
                <Select
                  v-model="form.marca_id"
                  :options="catalogOptions.marcas"
                  option-label="nombre"
                  option-value="id"
                  placeholder="Seleccionar"
                  filter
                  :filter-fields="['nombre']"
                  show-clear
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Presentacion</span>
                <InputText
                  v-model.trim="form.presentacion"
                  maxlength="100"
                  @input="form.presentacion = toUpperValue(form.presentacion)"
                  @focus="selectField"
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Referencia</span>
                <InputText
                  v-model.trim="form.referencia_producto"
                  maxlength="120"
                  @input="form.referencia_producto = toUpperValue(form.referencia_producto)"
                  @focus="selectField"
                />
              </div>
            </div>
          </div>

          <div v-else class="odoo-sheet-section">
            <div class="products-money-policy">
              Politica monetaria activa: costos y precios en {{ currencyLabel }}.
            </div>
            <div class="odoo-field-grid">
              <div class="odoo-field">
                <span class="odoo-field-label">Costo ({{ currencySymbol }})</span>
                <InputNumber
                  v-model="form.costo_producto"
                  mode="decimal"
                  :min="0"
                  :min-fraction-digits="2"
                  :max-fraction-digits="2"
                  :use-grouping="true"
                  input-class="erp-number-input"
                  @focus="selectField"
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Precio venta 1 ({{ currencySymbol }})</span>
                <InputNumber
                  v-model="form.precio_venta1"
                  mode="decimal"
                  :min="0"
                  :min-fraction-digits="2"
                  :max-fraction-digits="2"
                  :use-grouping="true"
                  input-class="erp-number-input"
                  @focus="selectField"
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Precio venta 2 ({{ currencySymbol }})</span>
                <InputNumber
                  v-model="form.precio_venta2"
                  mode="decimal"
                  :min="0"
                  :min-fraction-digits="2"
                  :max-fraction-digits="2"
                  :use-grouping="true"
                  input-class="erp-number-input"
                  @focus="selectField"
                />
              </div>

              <div class="odoo-field">
                <span class="odoo-field-label">Precio venta 3 ({{ currencySymbol }})</span>
                <InputNumber
                  v-model="form.precio_venta3"
                  mode="decimal"
                  :min="0"
                  :min-fraction-digits="2"
                  :max-fraction-digits="2"
                  :use-grouping="true"
                  input-class="erp-number-input"
                  @focus="selectField"
                />
              </div>

              <template v-if="!editingProductId">
                <div class="odoo-field">
                  <span class="odoo-field-label">Existencia inicial</span>
                  <InputNumber
                    v-model="form.existencia"
                    :min="0"
                    :min-fraction-digits="2"
                    :max-fraction-digits="2"
                    :use-grouping="false"
                    input-class="erp-number-input"
                    @focus="selectField"
                  />
                </div>

                <div class="odoo-field">
                  <span class="odoo-field-label">Bodega inicial</span>
                  <Select
                    v-model="form.bodega_inicial_id"
                    :options="catalogOptions.bodegas"
                    option-label="name"
                    option-value="id"
                    placeholder="Seleccionar"
                    filter
                    :filter-fields="['name', 'code']"
                    show-clear
                  />
                </div>
              </template>
            </div>
          </div>
        </div>

        <p v-if="formError" class="auth-error">{{ formError }}</p>

        <div class="product-form-actions">
          <Button type="button" label="Cancelar" severity="secondary" variant="outlined" @click="closeDialog" />
          <Button type="submit" :label="saving ? 'Guardando...' : editingProductId ? 'Actualizar' : 'Crear producto'" :loading="saving" />
        </div>
      </form>
    </Dialog>

    <Dialog
      v-model:visible="brandDialogVisible"
      modal
      header="Catalogo de marcas"
      :style="{ width: 'min(680px, 94vw)' }"
    >
      <div class="settings-env-layout">
        <form class="settings-env-form" @submit.prevent="submitBrand">
          <div class="product-form-grid">
            <label class="field-group field-span-2">
              <span>Marca</span>
              <input
                v-model.trim="brandForm.nombre"
                class="form-control"
                type="text"
                maxlength="120"
                @input="brandForm.nombre = toUpperValue(brandForm.nombre)"
              />
            </label>

            <label class="products-checkbox">
              <input v-model="brandForm.activo" type="checkbox" />
              <span>Activo</span>
            </label>
          </div>

          <div class="product-form-actions">
            <Button type="button" severity="secondary" variant="outlined" @click="resetBrandForm">
              Limpiar
            </Button>
            <Button :disabled="brandSaving" type="submit">
              {{ brandSaving ? "Guardando..." : brandForm.id ? "Actualizar marca" : "Agregar marca" }}
            </Button>
          </div>
          <p v-if="brandError" class="auth-error">{{ brandError }}</p>
        </form>

        <div class="settings-env-list">
          <div
            v-for="marca in catalogOptions.marcas"
            :key="marca.id"
            class="settings-env-card"
            :class="{ active: marca.activo }"
          >
            <div class="settings-env-head">
              <div>
                <strong>{{ marca.nombre }}</strong>
                <span>{{ marca.activo ? "Marca activa" : "Marca inactiva" }}</span>
              </div>
              <Tag :severity="marca.activo ? 'success' : 'contrast'" :value="marca.activo ? 'Activa' : 'Inactiva'" />
            </div>

            <div class="settings-env-actions">
              <Button type="button" severity="secondary" variant="outlined" size="small" @click="editBrand(marca)">
                Editar
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Dialog>

    <Dialog
      v-model:visible="catalogDialogVisible"
      modal
      header="Subcatalogos de productos"
      :style="{ width: 'min(820px, 96vw)' }"
      class="catalog-dialog"
    >
      <div class="catalog-workspace">
        <section class="catalog-editor-card">
          <div class="catalog-editor-head">
            <div>
              <span class="products-section-kicker">Mantenimiento</span>
              <h3>{{ catalogSectionMeta.title }}</h3>
              <p>{{ catalogSectionMeta.caption }}</p>
            </div>
            <Tag severity="contrast" :value="`${currentCatalogItems.length} registros`" rounded />
          </div>

          <div class="odoo-notebook-tabs catalog-tabs" role="tablist" aria-label="Subcatalogos">
            <button type="button" class="odoo-tab" :class="{ active: currentCatalogTab === 'lineas' }" @click="switchCatalogTab('lineas')">
              Lineas
            </button>
            <button type="button" class="odoo-tab" :class="{ active: currentCatalogTab === 'segmentos' }" @click="switchCatalogTab('segmentos')">
              Segmentos
            </button>
            <button type="button" class="odoo-tab" :class="{ active: currentCatalogTab === 'unidades' }" @click="switchCatalogTab('unidades')">
              Unidades
            </button>
          </div>

          <form class="catalog-editor-form" @submit.prevent="submitCatalog">
            <div v-if="currentCatalogTab === 'lineas'" class="catalog-form-grid">
              <label class="field-group">
                <span>Codigo</span>
                <input v-model.trim="catalogForm.cod_linea" class="form-control" type="text" maxlength="50" @input="catalogForm.cod_linea = toUpperValue(catalogForm.cod_linea)" />
              </label>
              <label class="field-group field-span-2">
                <span>Linea</span>
                <input v-model.trim="catalogForm.linea" class="form-control" type="text" maxlength="120" @input="catalogForm.linea = toUpperValue(catalogForm.linea)" />
              </label>
              <label class="products-checkbox">
                <input v-model="catalogForm.activo" type="checkbox" />
                <span>Activo</span>
              </label>
            </div>

            <div v-else-if="currentCatalogTab === 'segmentos'" class="catalog-form-grid catalog-form-grid-segment">
              <label class="field-group field-span-2">
                <span>Segmento</span>
                <input v-model.trim="catalogForm.segmento" class="form-control" type="text" maxlength="120" @input="catalogForm.segmento = toUpperValue(catalogForm.segmento)" />
              </label>
              <label class="products-checkbox">
                <input v-model="catalogForm.activo" type="checkbox" />
                <span>Activo</span>
              </label>
            </div>

            <div v-else class="catalog-form-grid">
              <label class="field-group">
                <span>Codigo</span>
                <input v-model.trim="catalogForm.codigo" class="form-control" type="text" maxlength="20" @input="catalogForm.codigo = toUpperValue(catalogForm.codigo)" />
              </label>
              <label class="field-group">
                <span>Nombre</span>
                <input v-model.trim="catalogForm.nombre" class="form-control" type="text" maxlength="80" @input="catalogForm.nombre = toUpperValue(catalogForm.nombre)" />
              </label>
              <label class="field-group">
                <span>Abreviatura</span>
                <input v-model.trim="catalogForm.abreviatura" class="form-control" type="text" maxlength="20" @input="catalogForm.abreviatura = toUpperValue(catalogForm.abreviatura)" />
              </label>
              <label class="products-checkbox">
                <input v-model="catalogForm.activo" type="checkbox" />
                <span>Activo</span>
              </label>
            </div>

            <div class="catalog-form-actions">
              <Button type="button" severity="secondary" variant="outlined" @click="resetCatalogForm">
                Limpiar
              </Button>
              <Button :disabled="catalogSaving" type="submit">
                {{ catalogSaving ? "Guardando..." : catalogForm.id ? "Actualizar" : "Agregar" }}
              </Button>
            </div>
            <p v-if="catalogError" class="auth-error">{{ catalogError }}</p>
          </form>
        </section>

        <section class="catalog-list-card">
          <div class="catalog-list-head">
            <div>
              <span class="products-section-kicker">Disponibles</span>
              <h3>Registros del catalogo</h3>
            </div>
          </div>

          <div class="catalog-list-scroll">
          <div
            v-for="item in currentCatalogItems"
            :key="item.id"
            class="settings-env-card catalog-record-card"
            :class="{ active: item.activo }"
          >
            <div class="settings-env-head">
              <div>
                <strong>{{ currentCatalogTitle(item) }}</strong>
                <span>{{ currentCatalogSubtitle(item) }}</span>
              </div>
              <Tag :severity="item.activo ? 'success' : 'contrast'" :value="item.activo ? 'Activo' : 'Inactivo'" />
            </div>

            <div class="settings-env-actions">
              <Button type="button" severity="secondary" variant="outlined" size="small" @click="editCatalogItem(item)">
                Editar
              </Button>
            </div>
          </div>
          </div>
        </section>
      </div>
    </Dialog>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import Checkbox from "primevue/checkbox";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import Dialog from "primevue/dialog";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import Tag from "primevue/tag";

import {
  createProduct,
  createLinea,
  createMarca,
  createSegmento,
  createUnidadMedida,
  fetchInventoryCatalogs,
  fetchNextProductCode,
  fetchProducts,
  toggleProductActive,
  updateLinea,
  updateMarca,
  updateSegmento,
  updateProduct,
  updateUnidadMedida,
} from "../../services/inventory";
import { readStoredUser } from "../../services/auth";
import { readStoredBusinessSettings } from "../../services/settings";

const search = ref("");
const showInactive = ref(false);
const loading = ref(true);
const error = ref("");
const products = ref([]);
const dialogVisible = ref(false);
const saving = ref(false);
const brandSaving = ref(false);
const formError = ref("");
const brandError = ref("");
const editingProductId = ref(null);
const currentFormTab = ref("general");
const brandDialogVisible = ref(false);
const catalogDialogVisible = ref(false);
const currentCatalogTab = ref("lineas");
const catalogSaving = ref(false);
const catalogError = ref("");
const currentUser = readStoredUser();
const businessSettings = readStoredBusinessSettings() || {};
const catalogs = reactive({
  lineas: 0,
  segmentos: 0,
  unidades: 0,
  bodegas: 0,
});
const catalogOptions = reactive({
  lineas: [],
  segmentos: [],
  unidades: [],
  marcas: [],
  bodegas: [],
});
const brandForm = reactive(getEmptyBrandForm());
const catalogForm = reactive(getEmptyCatalogForm());
const form = reactive(getEmptyForm());

const filteredProducts = computed(() => {
  const query = search.value.trim().toLowerCase();
  return products.value.filter((product) => {
    const matchesStatus = showInactive.value ? true : product.activo;
    const matchesQuery =
      !query ||
      (product.cod_producto || "").toLowerCase().includes(query) ||
      (product.descripcion || "").toLowerCase().includes(query);
    return matchesStatus && matchesQuery;
  });
});

const activeCount = computed(() => products.value.filter((item) => item.activo).length);
const inactiveCount = computed(() => products.value.filter((item) => !item.activo).length);
const pricingCurrency = computed(() =>
  (businessSettings?.pricing_currency || "CS").toUpperCase() === "USD" ? "USD" : "CS",
);
const currencySymbol = computed(() => (pricingCurrency.value === "USD" ? "US$" : "C$"));
const currencyLabel = computed(() => (pricingCurrency.value === "USD" ? "Dolares (USD)" : "Cordobas (C$)"));
const currentCatalogItems = computed(() => {
  if (currentCatalogTab.value === "lineas") return catalogOptions.lineas;
  if (currentCatalogTab.value === "segmentos") return catalogOptions.segmentos;
  return catalogOptions.unidades;
});
const catalogSectionMeta = computed(() => {
  if (currentCatalogTab.value === "lineas") {
    return {
      title: "Lineas de producto",
      caption: "Agrupa articulos por familia principal para operacion y reportes.",
    };
  }
  if (currentCatalogTab.value === "segmentos") {
    return {
      title: "Segmentos operativos",
      caption: "Clasifica productos por tipo comercial o comportamiento de venta.",
    };
  }
  return {
    title: "Unidades de medida",
    caption: "Configura codigos, nombres y abreviaturas para inventario y facturacion.",
  };
});
function getEmptyForm() {
  return {
    cod_producto: "",
    usa_codigo_barra: false,
    codigo_barra: "",
    descripcion: "",
    segmento_id: null,
    linea_id: null,
    unidad_medida_id: null,
    marca_id: null,
    marca: "",
    presentacion: "",
    precio_venta1: 0,
    precio_venta2: 0,
    precio_venta3: 0,
    activo: true,
    servicio_producto: false,
    es_por_peso: false,
    costo_producto: 0,
    referencia_producto: "",
    usuario_registro: currentUser?.email || "sistema",
    maquina_registro: "frontend",
    existencia: 0,
    bodega_inicial_id: null,
  };
}

function getEmptyBrandForm() {
  return {
    id: null,
    nombre: "",
    activo: true,
  };
}

function getEmptyCatalogForm() {
  return {
    id: null,
    cod_linea: "",
    linea: "",
    segmento: "",
    codigo: "",
    nombre: "",
    abreviatura: "",
    activo: true,
  };
}

function resetForm() {
  Object.assign(form, getEmptyForm());
  formError.value = "";
  editingProductId.value = null;
  currentFormTab.value = "general";
}

function resetBrandForm() {
  Object.assign(brandForm, getEmptyBrandForm());
  brandError.value = "";
}

function resetCatalogForm() {
  Object.assign(catalogForm, getEmptyCatalogForm());
  catalogError.value = "";
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

function selectField(event) {
  const target = event?.target || event?.originalEvent?.target;
  if (target && typeof target.select === "function") {
    requestAnimationFrame(() => target.select());
  }
}

function toUpperValue(value) {
  return (value || "").toUpperCase();
}

async function loadData() {
  loading.value = true;
  error.value = "";

  try {
    const [catalogData, productData] = await Promise.all([
      fetchInventoryCatalogs(),
      fetchProducts("", true),
    ]);

    catalogs.lineas = catalogData.lineas.length;
    catalogs.segmentos = catalogData.segmentos.length;
    catalogs.unidades = catalogData.unidades_medida.length;
    catalogs.marcas = catalogData.marcas.length;
    catalogs.bodegas = catalogData.bodegas.length;
    catalogOptions.lineas = catalogData.lineas;
    catalogOptions.segmentos = catalogData.segmentos;
    catalogOptions.unidades = catalogData.unidades_medida;
    catalogOptions.marcas = catalogData.marcas;
    catalogOptions.bodegas = catalogData.bodegas;
    products.value = productData;
  } catch (err) {
    error.value = err.message || "No se pudo cargar el catalogo";
  } finally {
    loading.value = false;
  }
}

async function openCreateDialog() {
  resetForm();
  dialogVisible.value = true;
  form.cod_producto = "";
  try {
    const nextCode = await fetchNextProductCode();
    form.cod_producto = nextCode.code || "";
  } catch {
    form.cod_producto = "";
  }
}

function openEditDialog(product) {
  resetForm();
  editingProductId.value = product.id;
  Object.assign(form, {
    cod_producto: product.cod_producto || "",
    usa_codigo_barra: Boolean(product.usa_codigo_barra),
    codigo_barra: product.codigo_barra || "",
    descripcion: product.descripcion || "",
    segmento_id: product.segmento_id ?? null,
    linea_id: product.linea_id ?? null,
    unidad_medida_id: product.unidad_medida_id ?? null,
    marca_id: product.marca_id ?? null,
    marca: product.marca || "",
    presentacion: product.presentacion || "",
    precio_venta1: Number(product.precio_venta1 || 0),
    precio_venta2: Number(product.precio_venta2 || 0),
    precio_venta3: Number(product.precio_venta3 || 0),
    activo: Boolean(product.activo),
    servicio_producto: Boolean(product.servicio_producto),
    es_por_peso: Boolean(product.es_por_peso),
    costo_producto: Number(product.costo_producto || 0),
    referencia_producto: product.referencia_producto || "",
    usuario_registro: currentUser?.email || "sistema",
    maquina_registro: "frontend",
    existencia: Number(product.saldo?.existencia || 0),
    bodega_inicial_id: null,
  });
  currentFormTab.value = "general";
  dialogVisible.value = true;
}

function closeDialog() {
  dialogVisible.value = false;
  resetForm();
}

function buildPayload() {
  return {
    cod_producto: form.cod_producto,
    usa_codigo_barra: Boolean(form.usa_codigo_barra),
    codigo_barra: form.usa_codigo_barra ? form.codigo_barra || null : null,
    descripcion: form.descripcion,
    segmento_id: form.segmento_id,
    linea_id: form.linea_id,
    unidad_medida_id: form.unidad_medida_id,
    marca_id: form.marca_id,
    marca: form.marca || null,
    presentacion: form.presentacion || null,
    precio_venta1: Number(form.precio_venta1 || 0),
    precio_venta2: Number(form.precio_venta2 || 0),
    precio_venta3: Number(form.precio_venta3 || 0),
    activo: Boolean(form.activo),
    servicio_producto: Boolean(form.servicio_producto),
    es_por_peso: Boolean(form.es_por_peso),
    costo_producto: Number(form.costo_producto || 0),
    referencia_producto: form.referencia_producto || null,
    usuario_registro: form.usuario_registro,
    maquina_registro: form.maquina_registro,
    ...(editingProductId.value
      ? {}
      : {
          existencia: Number(form.existencia || 0),
          bodega_inicial_id: form.bodega_inicial_id,
        }),
  };
}

function handleBarcodeToggle() {
  if (!form.usa_codigo_barra) {
    form.codigo_barra = "";
  }
}

async function submitForm() {
  saving.value = true;
  formError.value = "";
  try {
    const payload = buildPayload();
    if (editingProductId.value) {
      await updateProduct(editingProductId.value, payload);
    } else {
      await createProduct(payload);
    }
    await loadData();
    closeDialog();
  } catch (err) {
    formError.value = err.message || "No se pudo guardar el producto";
  } finally {
    saving.value = false;
  }
}

async function toggleActive(product) {
  try {
    await toggleProductActive(product.id);
    await loadData();
  } catch (err) {
    error.value = err.message || "No se pudo actualizar el estado";
  }
}

function openBrandDialog() {
  resetBrandForm();
  brandDialogVisible.value = true;
}

function openCatalogDialog() {
  resetCatalogForm();
  currentCatalogTab.value = "lineas";
  catalogDialogVisible.value = true;
}

function switchCatalogTab(tab) {
  currentCatalogTab.value = tab;
  resetCatalogForm();
}

function editBrand(marca) {
  brandForm.id = marca.id;
  brandForm.nombre = marca.nombre || "";
  brandForm.activo = Boolean(marca.activo);
  brandError.value = "";
}

async function submitBrand() {
  brandSaving.value = true;
  brandError.value = "";
  try {
    const payload = {
      nombre: brandForm.nombre,
      activo: Boolean(brandForm.activo),
    };
    if (brandForm.id) {
      await updateMarca(brandForm.id, payload);
    } else {
      await createMarca(payload);
    }
    await loadData();
    resetBrandForm();
  } catch (err) {
    brandError.value = err.message || "No se pudo guardar la marca";
  } finally {
    brandSaving.value = false;
  }
}

function currentCatalogTitle(item) {
  if (currentCatalogTab.value === "lineas") return item.linea;
  if (currentCatalogTab.value === "segmentos") return item.segmento;
  return item.nombre;
}

function currentCatalogSubtitle(item) {
  if (currentCatalogTab.value === "lineas") return item.cod_linea || "Sin codigo";
  if (currentCatalogTab.value === "segmentos") return "Segmento operativo";
  return `${item.codigo || ""}${item.abreviatura ? ` · ${item.abreviatura}` : ""}`.trim();
}

function editCatalogItem(item) {
  resetCatalogForm();
  if (currentCatalogTab.value === "lineas") {
    Object.assign(catalogForm, {
      id: item.id,
      cod_linea: item.cod_linea || "",
      linea: item.linea || "",
      activo: Boolean(item.activo),
    });
    return;
  }
  if (currentCatalogTab.value === "segmentos") {
    Object.assign(catalogForm, {
      id: item.id,
      segmento: item.segmento || "",
      activo: Boolean(item.activo),
    });
    return;
  }
  Object.assign(catalogForm, {
    id: item.id,
    codigo: item.codigo || "",
    nombre: item.nombre || "",
    abreviatura: item.abreviatura || "",
    activo: Boolean(item.activo),
  });
}

async function submitCatalog() {
  catalogSaving.value = true;
  catalogError.value = "";
  try {
    if (currentCatalogTab.value === "lineas") {
      const payload = {
        cod_linea: catalogForm.cod_linea,
        linea: catalogForm.linea,
        activo: Boolean(catalogForm.activo),
      };
      if (catalogForm.id) await updateLinea(catalogForm.id, payload);
      else await createLinea(payload);
    } else if (currentCatalogTab.value === "segmentos") {
      const payload = {
        segmento: catalogForm.segmento,
        activo: Boolean(catalogForm.activo),
      };
      if (catalogForm.id) await updateSegmento(catalogForm.id, payload);
      else await createSegmento(payload);
    } else {
      const payload = {
        codigo: catalogForm.codigo,
        nombre: catalogForm.nombre,
        abreviatura: catalogForm.abreviatura,
        activo: Boolean(catalogForm.activo),
      };
      if (catalogForm.id) await updateUnidadMedida(catalogForm.id, payload);
      else await createUnidadMedida(payload);
    }
    await loadData();
    resetCatalogForm();
  } catch (err) {
    catalogError.value = err.message || "No se pudo guardar el subcatalogo";
  } finally {
    catalogSaving.value = false;
  }
}

onMounted(async () => {
  await loadData();
});
</script>
