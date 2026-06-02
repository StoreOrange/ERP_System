<template>
  <section class="page-section sales-page">
    <header class="sales-header-shell panel-card">
      <div class="sales-header-top">
        <div class="sales-header-copy">
          <p class="page-kicker">Ecommerce</p>
          <h1 class="page-title">Terminal de venta empresarial</h1>
          <p class="panel-text">
            Arquitectura operativa basada en HollywoodPacas para facturacion, caja y busqueda
            rapida de articulos.
          </p>
        </div>

        <div class="sales-kpi-grid">
          <article class="sales-kpi-box">
            <span>Tasa</span>
            <strong>C$ {{ formatRate(rateToday) }}</strong>
          </article>
          <article class="sales-kpi-box">
            <span>Factura</span>
            <strong>{{ nextInvoice }}</strong>
          </article>
          <article class="sales-kpi-box">
            <span>Interfaz</span>
            <strong>{{ salesInterfaceLabel }}</strong>
          </article>
          <article class="sales-kpi-box">
            <span>Bodega</span>
            <strong>{{ currentBodegaLabel }}</strong>
          </article>
          <article class="sales-kpi-box">
            <span>Items</span>
            <strong>{{ saleItems.length }}</strong>
          </article>
          <article class="sales-kpi-box accent">
            <span>Total</span>
            <strong>{{ invoiceCurrencySymbol }} {{ formatMoney(invoiceTotal) }}</strong>
          </article>
        </div>
      </div>

      <div class="sales-tabbar">
        <button
          v-for="tab in salesTabs"
          :key="tab.key"
          type="button"
          class="sales-tab"
          :class="{ active: activeTab === tab.key, disabled: tab.disabled }"
          @click="setActiveTab(tab)"
        >
          {{ tab.label }}
        </button>
      </div>
    </header>

    <div v-if="salesAlert.message" class="sales-banner" :class="salesAlert.type">
      <i class="bi" :class="salesAlert.type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'"></i>
      <span>{{ salesAlert.message }}</span>
    </div>

    <form class="sales-shell" @submit.prevent>
      <div class="sales-grid">
        <div class="sales-main-column">
          <section class="panel-card sales-card sales-ticket-card">
            <div class="sales-card-head">
              <div>
                <span class="products-section-kicker">Facturacion virtual</span>
                <h3>Ticket actual</h3>
                <p>Vista virtual del ticket antes de confirmar la venta.</p>
              </div>
              <Tag severity="contrast" :value="`${saleItems.length} items seleccionados`" rounded />
            </div>

            <div class="sales-card-body">
            <div class="sales-ticket-table">
              <div class="sales-ticket-head">
                <span>Detalle del producto</span>
                <span>Quitar</span>
              </div>

              <div v-if="!saleItems.length" class="empty-state">Sin items agregados.</div>

              <div v-else class="sales-ticket-body">
                <article v-for="item in saleItems" :key="item.id" class="sales-ticket-row">
                  <div class="sales-ticket-detail">
                    <div class="sales-ticket-titleline">
                      <strong>{{ item.descripcion }}</strong>
                      <Tag :value="item.cod_producto" rounded />
                    </div>

                    <div class="sales-ticket-meta">
                      <span>{{ item.unidad_medida_abreviatura || "UND" }}</span>
                      <span>{{ item.codigo_barra || "SIN BARRA" }}</span>
                      <span>{{ itemCurrencyLabel(item) }}</span>
                      <span>{{ invoiceCurrencySymbol }} {{ formatMoney(item.subtotal) }}</span>
                    </div>

                    <div class="sales-ticket-editor">
                      <label class="sales-inline-field">
                        <span>Cant.</span>
                        <InputNumber
                          v-model="item.cantidad"
                          :min="0.01"
                          :step="item.es_por_peso ? 0.01 : 1"
                          :min-fraction-digits="item.es_por_peso ? 2 : 0"
                          :max-fraction-digits="item.es_por_peso ? 2 : 0"
                          input-class="erp-number-input"
                          @update:model-value="recalculateItem(item)"
                        />
                      </label>

                      <label class="sales-inline-field">
                        <span>Precio</span>
                        <InputNumber
                          v-model="item.precio"
                          :min="0"
                          :min-fraction-digits="2"
                          :max-fraction-digits="2"
                          input-class="erp-number-input"
                          @update:model-value="recalculateItem(item)"
                        />
                      </label>
                    </div>
                  </div>

                  <div class="sales-ticket-actions">
                    <Button
                      type="button"
                      icon="bi bi-trash3"
                      severity="danger"
                      variant="text"
                      rounded
                      @click="removeSaleItem(item.id)"
                    />
                  </div>
                </article>
              </div>
            </div>

            <div class="sales-summary-strip">
              <div class="sales-summary-chip">
                <span>Total USD</span>
                <strong>US$ {{ formatMoney(totalUsd) }}</strong>
              </div>
              <div class="sales-summary-chip">
                <span>Total C$</span>
                <strong>C$ {{ formatMoney(totalCs) }}</strong>
              </div>
              <div class="sales-summary-chip">
                <span>Items</span>
                <strong>{{ totalItems }}</strong>
              </div>
              <div class="sales-summary-chip">
                <span>Bultos</span>
                <strong>{{ totalBundles }}</strong>
              </div>
            </div>
            </div>
          </section>

          <section class="panel-card sales-card">
            <div class="sales-card-head">
              <div>
                <span class="products-section-kicker">Datos comerciales</span>
                <h3>Informacion de la factura</h3>
                <p>Configura cliente, vendedor y condiciones antes de registrar.</p>
              </div>
            </div>

            <div class="sales-card-body">
            <div class="sales-form-grid">
              <div class="sales-form-span-2 sales-customer-stack">
                <label class="field-group">
                  <span>Cliente</span>
                  <div class="sales-party-bar">
                    <Button
                      type="button"
                      severity="secondary"
                      variant="outlined"
                      size="small"
                      icon="bi bi-search"
                      label="Buscar cliente"
                      @click="customerDialog = true"
                    />
                    <div class="sales-party-selection">
                      <span class="sales-party-label">Seleccionado:</span>
                      <strong class="sales-party-value">{{ saleForm.customer_name || "Consumidor final" }}</strong>
                    </div>
                    <Button
                      class="sales-default-customer"
                      type="button"
                      severity="secondary"
                      variant="text"
                      size="small"
                      icon="bi bi-person-check"
                      label="Consumidor final"
                      aria-label="Usar consumidor final"
                      title="Usar consumidor final"
                      @click="setDefaultCustomer"
                    />
                    <Button
                      type="button"
                      severity="secondary"
                      variant="outlined"
                      size="small"
                      icon="bi bi-person-plus"
                      :label="showCustomerCreate ? 'Cerrar' : 'Nuevo cliente'"
                      @click="showCustomerCreate = !showCustomerCreate"
                    />
                  </div>
                </label>

                <div v-if="showCustomerCreate" class="sales-inline-create">
                  <div class="sales-inline-create-title">Nuevo cliente</div>
                  <div class="sales-customer-editor">
                    <input v-model="customerDraft.nombre" class="form-control" placeholder="Nombre del cliente *" />
                    <input v-model="customerDraft.telefono" class="form-control" placeholder="Telefono" />
                    <input v-model="customerDraft.identificacion" class="form-control" placeholder="RUC / Cedula" />
                    <input v-model="customerDraft.direccion" class="form-control sales-address-field" placeholder="Direccion" />
                  </div>
                  <div class="sales-inline-create-actions">
                    <Button type="button" icon="bi bi-person-plus" label="Guardar cliente" @click="saveCustomer" />
                  </div>
                </div>
              </div>

              <div class="sales-vendor-field">
                <label class="field-group">
                  <span>Vendedor</span>
                  <div class="sales-inline-actions">
                    <Select
                      v-model="saleForm.vendedor_id"
                      :options="vendors"
                      option-label="nombre"
                      option-value="id"
                      placeholder="Selecciona"
                      filter
                      :filter-fields="['nombre']"
                    />
                    <Button
                      type="button"
                      severity="secondary"
                      variant="outlined"
                      size="small"
                      icon="bi bi-person-plus"
                      @click="vendorDialog = true"
                    />
                  </div>
                </label>
              </div>

              <label class="field-group">
                <span>Fecha</span>
                <input v-model="saleForm.date" class="form-control" type="date" />
              </label>

              <label class="field-group">
                <span>Condicion de venta</span>
                <select v-model="saleForm.condition" class="form-control">
                  <option value="CONTADO">Contado</option>
                  <option value="CREDITO">Credito</option>
                </select>
              </label>

              <label class="field-group">
                <span>Bodega</span>
                <Select
                  v-model="saleForm.bodega_id"
                  :options="catalogs.bodegas"
                  option-label="name"
                  option-value="id"
                  placeholder="Seleccionar"
                  filter
                  :filter-fields="['name', 'code']"
                />
              </label>

              <label class="field-group sales-form-span-4">
                <span>Observacion</span>
                <input
                  v-model="saleForm.observacion"
                  class="form-control"
                  placeholder="Agrega una nota comercial opcional"
                />
              </label>
            </div>
            </div>
          </section>

          <div class="sales-footer-actions">
            <Button type="button" severity="secondary" variant="outlined" icon="bi bi-arrow-counterclockwise" label="Limpiar venta" @click="clearSale" />
            <Button type="button" icon="bi bi-check2-circle" label="Registrar venta" @click="openPaymentDialog" />
          </div>
        </div>

        <div class="sales-side-column">
          <section class="panel-card sales-card sales-search-card">
            <div class="sales-card-head">
              <div>
                <div class="sales-search-titlebar">
                  <h3>Catalogo de productos</h3>
                  <div class="sales-search-title-actions">
                    <Button type="button" severity="secondary" variant="outlined" size="small" icon="bi bi-boxes" label="Combos" />
                  </div>
                </div>

                <div class="sales-search-meta">
                  <span>Busca para cargar articulos al ticket.</span>
                  <span class="scanner-badge" :class="scannerState">
                    <i class="bi bi-upc-scan"></i>
                    {{ scannerLabel }}
                  </span>
                  <span class="scanner-last">Ultimo: {{ lastScannedCode || "-" }}</span>
                  <div class="sales-price-inline">
                    <label for="sales-price-list">Lista:</label>
                    <select id="sales-price-list" v-model="saleForm.price_list" class="form-control sales-price-list">
                      <option v-for="option in priceLists" :key="option.value" :value="option.value">
                        {{ option.label }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <div class="sales-card-body">
            <div class="sales-search-inputshell" :class="{ 'barcode-ready': scannerState === 'working' }">
              <i class="bi bi-search"></i>
              <InputText
                ref="searchInputRef"
                v-model="searchQuery"
                class="search-input"
                type="search"
                placeholder="BUSCAR PRODUCTO"
                @keydown.down.prevent="moveSearchSelection(1)"
                @keydown.up.prevent="moveSearchSelection(-1)"
                @keydown.enter.prevent="handleSearchEnter"
              />
            </div>

            <div ref="searchPanelRef" class="sales-search-panel" tabindex="0" role="listbox" aria-label="Resultados de productos">
              <div class="sales-search-head">
                <span>Producto</span>
                <span>Cargar</span>
              </div>

              <div v-if="searchingProducts" class="empty-state">Buscando productos...</div>
              <div v-else-if="searchQuery.trim().length < 2" class="empty-state">Escribe para buscar productos.</div>
              <div v-else-if="searchResults.length === 0" class="empty-state">Sin resultados para esta busqueda.</div>

              <div v-else class="sales-search-results">
                <button
                  v-for="(item, index) in searchResults"
                  :key="item.id"
                  type="button"
                  class="sales-search-item"
                  :class="{ active: searchActiveIndex === index }"
                  @click="addProductToSale(item)"
                >
                  <div class="sales-search-itemcopy">
                    <strong>{{ item.descripcion }}</strong>
                    <span>
                      {{ item.cod_producto }}
                      <template v-if="item.codigo_barra"> &middot; {{ item.codigo_barra }}</template>
                    </span>
                  </div>

                  <div class="sales-search-itemmeta">
                    <strong>{{ invoiceCurrencySymbol }} {{ formatMoney(resolvePrice(item)) }}</strong>
                    <small>Stock: {{ formatQty(item.existencia) }}</small>
                  </div>
                </button>
              </div>
            </div>
            </div>
          </section>
        </div>
      </div>
    </form>

    <Dialog v-model:visible="paymentDialog" modal :style="{ width: 'min(1180px, 96vw)' }" class="sales-payment-dialog">
      <template #header>
        <div class="sales-payment-title">
          <span class="products-section-kicker">Procesar pago</span>
          <h3>Resumen y formas de pago</h3>
        </div>
      </template>

      <div class="sales-payment-grid">
        <section class="panel-card sales-payment-card">
          <div class="sales-card-head">
            <div>
              <span class="products-section-kicker">Resumen</span>
              <h3>Resumen de venta</h3>
            </div>
          </div>

          <div class="sales-card-body">
          <div class="sales-pay-summary">
            <div class="sales-pay-row"><span>Cliente</span><strong>{{ saleForm.customer_name || "Consumidor final" }}</strong></div>
            <div class="sales-pay-row"><span>Vendedor</span><strong>{{ selectedVendorName }}</strong></div>
            <div class="sales-pay-row"><span>Factura</span><strong>{{ nextInvoice }}</strong></div>
            <div class="sales-pay-row"><span>Fecha</span><strong>{{ saleForm.date }}</strong></div>
            <div class="sales-pay-row"><span>Hora</span><strong>{{ currentTimeLabel }}</strong></div>
          </div>

          <div class="sales-pay-totals sales-pay-totals-compact">
            <div class="sales-pay-totalbox">
              <span>Total USD</span>
              <strong>US$ {{ formatMoney(totalUsd) }}</strong>
            </div>
            <div class="sales-pay-totalbox">
              <span>Total C$</span>
              <strong>C$ {{ formatMoney(totalCs) }}</strong>
            </div>
          </div>

          <div class="sales-payment-formgrid">
            <label class="field-group">
              <span>Moneda de la factura</span>
              <select v-model="saleForm.invoice_currency" class="form-control">
                <option value="CS">C$</option>
                <option value="USD">USD</option>
              </select>
            </label>
            <label class="field-group">
              <span>Lista de precio</span>
              <select v-model="saleForm.price_list" class="form-control">
                <option v-for="option in priceLists" :key="option.value" :value="option.value">
                  {{ option.longLabel }}
                </option>
              </select>
            </label>
          </div>

          <div class="sales-pay-balance">
            <div class="sales-pay-row"><span>Total venta</span><strong>{{ invoiceCurrencySymbol }} {{ formatMoney(invoiceTotal) }}</strong></div>
            <div class="sales-pay-row"><span>Pagado</span><strong>{{ invoiceCurrencySymbol }} {{ formatMoney(totalPaidInInvoiceCurrency) }}</strong></div>
            <div class="sales-pay-row"><span>Saldo / Vuelto</span><strong :class="paymentBalance < 0 ? 'balance-positive' : 'balance-negative'">{{ invoiceCurrencySymbol }} {{ formatMoney(Math.abs(paymentBalance)) }}</strong></div>
          </div>
          </div>
        </section>

        <section class="panel-card sales-payment-card">
          <div class="sales-card-head">
            <div>
              <span class="products-section-kicker">Pago rapido</span>
              <h3>Formas de pago</h3>
              <p v-if="saleForm.condition === 'CREDITO'">Venta a credito: no se registran pagos en esta pantalla.</p>
            </div>
          </div>

          <div class="sales-card-body">
          <div v-if="saleForm.condition !== 'CREDITO'" class="sales-methods-grid">
            <button
              v-for="method in paymentMethods"
              :key="method.id"
              type="button"
              class="sales-method-btn"
              :class="{ active: paymentDraft.forma_id === method.id }"
              @click="selectPaymentMethod(method)"
            >
              <i :class="method.icon"></i>
              <span>{{ method.label }}</span>
            </button>
          </div>

          <div v-if="saleForm.condition !== 'CREDITO'" class="sales-payment-formgrid payment-grid-wide">
            <label class="field-group">
              <span>Moneda</span>
              <select v-model="paymentDraft.moneda" class="form-control">
                <option value="CS">C$</option>
                <option value="USD">USD</option>
              </select>
            </label>
            <label class="field-group">
              <span>Monto</span>
              <InputNumber
                v-model="paymentDraft.monto"
                :min="0"
                :min-fraction-digits="2"
                :max-fraction-digits="2"
                input-class="erp-number-input"
              />
            </label>
            <label v-if="showBankFields" class="field-group">
              <span>Banco</span>
              <Select
                v-model="paymentDraft.banco_id"
                :options="banks"
                option-label="nombre"
                option-value="id"
                placeholder="Selecciona"
              />
            </label>
            <label v-if="showBankFields" class="field-group">
              <span>Cuenta</span>
              <Select
                v-model="paymentDraft.cuenta_id"
                :options="filteredAccounts"
                option-label="label"
                option-value="id"
                placeholder="Selecciona"
              />
            </label>
          </div>

          <div v-if="saleForm.condition !== 'CREDITO'" class="sales-payment-actions">
            <Button type="button" severity="secondary" variant="outlined" icon="bi bi-calculator" label="Completar saldo" @click="fillRemainingAmount" />
            <Button type="button" icon="bi bi-plus-lg" label="Agregar pago" @click="addPayment" />
          </div>

          <div class="sales-payments-list">
            <div class="sales-card-head">
              <div>
                <span class="products-section-kicker">Pagos aplicados</span>
                <h3>Detalle</h3>
              </div>
            </div>

            <div v-if="!payments.length" class="empty-state">Sin pagos agregados.</div>

            <div v-else class="sales-payment-table">
              <article v-for="payment in payments" :key="payment.id" class="sales-payment-row">
                <div class="sales-payment-copy">
                  <strong>{{ payment.forma_label }}</strong>
                  <span>{{ payment.moneda }} &middot; {{ payment.bank_label || "Sin banco" }}</span>
                </div>

                <div class="sales-payment-amount">
                  <strong>{{ payment.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(payment.monto) }}</strong>
                  <Button
                    type="button"
                    icon="bi bi-trash3"
                    severity="danger"
                    variant="text"
                    rounded
                    @click="removePayment(payment.id)"
                  />
                </div>
              </article>
            </div>
          </div>
          </div>
        </section>
      </div>

      <template #footer>
        <div class="sales-payment-footer">
          <Button type="button" severity="secondary" variant="outlined" label="Cancelar" @click="paymentDialog = false" />
          <Button type="button" icon="bi bi-check2-circle" label="Confirmar y registrar factura" @click="confirmSale" />
        </div>
      </template>
    </Dialog>

    <Dialog v-model:visible="customerDialog" modal :style="{ width: 'min(760px, 94vw)' }" class="sales-helper-dialog">
      <template #header>
        <div class="sales-payment-title">
          <span class="products-section-kicker">Clientes</span>
          <h3>Buscar cliente</h3>
        </div>
      </template>

      <div class="sales-helper-grid">
        <label class="field-group sales-helper-search">
          <span>Buscar cliente</span>
          <input v-model="customerSearch" class="form-control" placeholder="Escribe para buscar..." />
        </label>

        <div class="sales-helper-list">
          <div v-if="!filteredCustomers.length" class="empty-state">Sin resultados.</div>
          <button
            v-for="customer in filteredCustomers"
            :key="customer.id"
            type="button"
            class="sales-helper-item"
            @click="selectCustomer(customer)"
          >
            <strong>{{ customer.nombre }}</strong>
            <span>{{ customer.identificacion || customer.telefono || "Sin dato adicional" }}</span>
          </button>
        </div>
      </div>
    </Dialog>

    <Dialog v-model:visible="vendorDialog" modal :style="{ width: 'min(520px, 92vw)' }" class="sales-helper-dialog">
      <template #header>
        <div class="sales-payment-title">
          <span class="products-section-kicker">Vendedores</span>
          <h3>Nuevo vendedor</h3>
        </div>
      </template>

      <div class="sales-vendor-dialog">
        <label class="field-group">
          <span>Nombre del vendedor</span>
          <input v-model="vendorDraft.nombre" class="form-control" placeholder="Nombre del vendedor *" />
        </label>
        <div class="sales-payment-footer">
          <Button type="button" severity="secondary" variant="outlined" label="Cancelar" @click="vendorDialog = false" />
          <Button type="button" icon="bi bi-person-plus" label="Guardar vendedor" @click="saveVendor" />
        </div>
      </div>
    </Dialog>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import Tag from "primevue/tag";

import { readStoredUser } from "../../services/auth";
import { fetchInventoryCatalogs, searchInventoryProducts } from "../../services/inventory";
import { fetchPublicBusinessSettings } from "../../services/settings";

const currentUser = readStoredUser();
const paymentDialog = ref(false);
const customerDialog = ref(false);
const vendorDialog = ref(false);
const searchingProducts = ref(false);
const showCustomerCreate = ref(false);
const searchQuery = ref("");
const searchResults = ref([]);
const searchActiveIndex = ref(-1);
const searchTimeout = ref(null);
const searchInputRef = ref(null);
const searchPanelRef = ref(null);
const activeTab = ref("sales");
const currentTimeLabel = ref(formatTimeNow());
const scannerState = ref("idle");
const scannerLabel = ref("Lector listo");
const lastScannedCode = ref("");
const barcodeBuffer = ref("");
const barcodeResetTimer = ref(null);
const catalogs = reactive({ bodegas: [] });
const businessSettings = reactive({ sales_interface_code: "ropa" });
const saleItems = ref([]);
const payments = ref([]);
const salesAlert = reactive({ type: "success", message: "" });
const customerSearch = ref("");

const priceLists = [
  { value: "1", label: "P1", longLabel: "Precio 1 (base)" },
  { value: "2", label: "P2", longLabel: "Precio 2" },
  { value: "3", label: "P3", longLabel: "Precio 3" },
  { value: "4", label: "P4", longLabel: "Precio 4" },
  { value: "5", label: "P5", longLabel: "Precio 5" },
  { value: "6", label: "P6", longLabel: "Precio 6" },
  { value: "7", label: "P7", longLabel: "Precio 7" },
];

const salesTabs = [
  { key: "sales", label: "Ventas", disabled: false },
  { key: "collections", label: "Cobranza", disabled: true },
  { key: "utility", label: "Utilitario", disabled: true },
  { key: "deposits", label: "Depositos", disabled: true },
  { key: "closing", label: "Cierre", disabled: true },
];

const saleForm = reactive({
  customer_id: null,
  customer_name: "Consumidor final",
  customer_phone: "",
  customer_document: "",
  customer_address: "",
  vendedor_id: null,
  date: new Date().toISOString().slice(0, 10),
  condition: "CONTADO",
  observacion: "",
  bodega_id: null,
  invoice_currency: "CS",
  price_list: "1",
});

const customerDraft = reactive({
  nombre: "",
  telefono: "",
  identificacion: "",
  direccion: "",
});

const vendorDraft = reactive({
  nombre: "",
});

const customers = ref([
  { id: 1, nombre: "Consumidor final", telefono: "", identificacion: "", direccion: "" },
]);

const vendors = ref([
  { id: 1, nombre: currentUser?.full_name || "Administrador" },
  { id: 2, nombre: "Vendedor de Tienda" },
]);

const paymentDraft = reactive({
  forma_id: "cash",
  moneda: "CS",
  monto: null,
  banco_id: null,
  cuenta_id: null,
});

const paymentMethods = [
  { id: "cash", label: "Efectivo", icon: "bi bi-cash-coin", needsBank: false },
  { id: "card", label: "Tarjeta", icon: "bi bi-credit-card", needsBank: false },
  { id: "transfer", label: "Transferencia", icon: "bi bi-bank", needsBank: true },
  { id: "deposit", label: "Deposito", icon: "bi bi-wallet2", needsBank: true },
];

const banks = [
  { id: 1, nombre: "BAC" },
  { id: 2, nombre: "LAFISE" },
  { id: 3, nombre: "BANPRO" },
];

const accounts = [
  { id: 1, banco_id: 1, moneda: "CS", label: "BAC - C$ 100200300" },
  { id: 2, banco_id: 1, moneda: "USD", label: "BAC - USD 100200301" },
  { id: 3, banco_id: 2, moneda: "CS", label: "LAFISE - C$ 204300501" },
  { id: 4, banco_id: 3, moneda: "USD", label: "BANPRO - USD 88991200" },
];

const nextInvoice = computed(() => `FAC-${String(saleItems.value.length + 1).padStart(5, "0")}`);
const salesInterfaceLabel = computed(() => {
  const found = {
    ropa: "Venta empresarial",
    zapatos: "POS Zapatos",
    restaurante: "POS Restaurante",
    comestibles: "POS Comestibles",
  }[businessSettings.sales_interface_code];
  return found || "Venta empresarial";
});
const rateToday = computed(() => 36.62);
const invoiceCurrencySymbol = computed(() => (saleForm.invoice_currency === "USD" ? "US$" : "C$"));
const currentBodegaLabel = computed(() => {
  const bodega = catalogs.bodegas.find((item) => item.id === saleForm.bodega_id);
  return bodega?.name || "-";
});
const totalUsd = computed(() => saleItems.value.reduce((sum, item) => sum + Number(item.subtotal_usd || 0), 0));
const totalCs = computed(() => saleItems.value.reduce((sum, item) => sum + Number(item.subtotal_cs || 0), 0));
const invoiceTotal = computed(() => (saleForm.invoice_currency === "USD" ? totalUsd.value : totalCs.value));
const totalItems = computed(() => saleItems.value.reduce((sum, item) => sum + Number(item.cantidad || 0), 0).toFixed(2));
const totalBundles = computed(() => saleItems.value.length);
const selectedVendorName = computed(() => vendors.value.find((item) => item.id === saleForm.vendedor_id)?.nombre || "Vendedor");
const totalPaidInInvoiceCurrency = computed(() =>
  payments.value.reduce((sum, payment) => {
    const rate = getRate();
    if (payment.moneda === saleForm.invoice_currency) return sum + Number(payment.monto || 0);
    if (payment.moneda === "USD" && saleForm.invoice_currency === "CS") return sum + Number(payment.monto || 0) * rate;
    if (payment.moneda === "CS" && saleForm.invoice_currency === "USD") return sum + (rate > 0 ? Number(payment.monto || 0) / rate : 0);
    return sum;
  }, 0),
);
const paymentBalance = computed(() => invoiceTotal.value - totalPaidInInvoiceCurrency.value);
const showBankFields = computed(() => paymentMethods.find((item) => item.id === paymentDraft.forma_id)?.needsBank || false);
const filteredAccounts = computed(() =>
  accounts.filter((item) => (!paymentDraft.banco_id || item.banco_id === paymentDraft.banco_id) && item.moneda === paymentDraft.moneda),
);
const filteredCustomers = computed(() => {
  const query = customerSearch.value.trim().toLowerCase();
  if (!query) return customers.value;
  return customers.value.filter((item) =>
    [item.nombre, item.identificacion, item.telefono].some((value) => String(value || "").toLowerCase().includes(query)),
  );
});

function getRate() {
  return Number(rateToday.value || 36.62);
}

function formatMoney(value) {
  return new Intl.NumberFormat("es-NI", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value || 0));
}

function formatRate(value) {
  return new Intl.NumberFormat("es-NI", {
    minimumFractionDigits: 4,
    maximumFractionDigits: 4,
  }).format(Number(value || 0));
}

function formatQty(value) {
  return Number(value || 0).toFixed(2);
}

function formatTimeNow() {
  return new Intl.DateTimeFormat("es-NI", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date());
}

function resolvePrice(item) {
  const priceTier = Number(saleForm.price_list || 1);
  const csPrice = Number(
    item[`precio_venta${priceTier}`] ??
      item.precio_venta1 ??
      item.selected_price_cs ??
      0,
  );
  if (saleForm.invoice_currency === "USD") {
    const usdCandidate = Number(item[`precio_venta${priceTier}_usd`] ?? item.selected_price_usd ?? 0);
    return usdCandidate || (getRate() > 0 ? csPrice / getRate() : 0);
  }
  return csPrice;
}

function itemCurrencyLabel(item) {
  return `${formatQty(item.cantidad)} x ${invoiceCurrencySymbol.value} ${formatMoney(item.precio)}`;
}

function recalculateItem(item) {
  const qty = Number(item.cantidad || 0);
  const price = Number(item.precio || 0);
  item.subtotal = qty * price;
  if (saleForm.invoice_currency === "USD") {
    item.subtotal_usd = item.subtotal;
    item.subtotal_cs = item.subtotal * getRate();
  } else {
    item.subtotal_cs = item.subtotal;
    item.subtotal_usd = getRate() > 0 ? item.subtotal / getRate() : 0;
  }
}

function normalizeProductForSale(product) {
  const price = resolvePrice(product);
  const qty = product.es_por_peso ? 0.01 : 1;
  const normalized = {
    id: `${product.id}-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
    product_id: product.id,
    cod_producto: product.cod_producto,
    codigo_barra: product.codigo_barra,
    descripcion: product.descripcion,
    unidad_medida_abreviatura: product.unidad_medida_abreviatura || "UND",
    es_por_peso: Boolean(product.es_por_peso),
    cantidad: qty,
    precio: price,
    subtotal: 0,
    subtotal_usd: 0,
    subtotal_cs: 0,
  };
  recalculateItem(normalized);
  return normalized;
}

function addProductToSale(product) {
  const currentPrice = Number(resolvePrice(product));
  const existing = saleItems.value.find((item) => item.product_id === product.id && Number(item.precio || 0) === currentPrice);
  if (existing) {
    existing.cantidad = Number(existing.cantidad || 0) + (product.es_por_peso ? 0.01 : 1);
    recalculateItem(existing);
  } else {
    saleItems.value.push(normalizeProductForSale(product));
  }
  lastScannedCode.value = product.codigo_barra || product.cod_producto || "";
  searchQuery.value = "";
  searchResults.value = [];
  searchActiveIndex.value = -1;
  scannerState.value = "working";
  scannerLabel.value = "Producto cargado";
  focusSearchInput();
  window.setTimeout(() => {
    scannerState.value = "idle";
    scannerLabel.value = "Lector listo";
  }, 600);
}

function removeSaleItem(itemId) {
  saleItems.value = saleItems.value.filter((item) => item.id !== itemId);
}

function moveSearchSelection(direction) {
  if (!searchResults.value.length) return;
  if (searchActiveIndex.value === -1) {
    searchActiveIndex.value = direction > 0 ? 0 : searchResults.value.length - 1;
  } else {
    searchActiveIndex.value = (searchActiveIndex.value + direction + searchResults.value.length) % searchResults.value.length;
  }
  scrollActiveSearchItemIntoView();
}

function handleSearchEnter() {
  if (!searchResults.value.length) return;
  const index = searchActiveIndex.value === -1 ? 0 : searchActiveIndex.value;
  addProductToSale(searchResults.value[index]);
}

function scrollActiveSearchItemIntoView() {
  nextTick(() => {
    const panel = searchPanelRef.value;
    const item = panel?.querySelector?.(".sales-search-item.active");
    item?.scrollIntoView?.({ block: "nearest" });
  });
}

function focusSearchInput() {
  nextTick(() => {
    const input = searchInputRef.value?.$el?.querySelector?.("input") || searchInputRef.value?.input || searchInputRef.value;
    input?.focus?.();
    input?.select?.();
  });
}

function setDefaultCustomer() {
  saleForm.customer_id = 1;
  saleForm.customer_name = "Consumidor final";
  saleForm.customer_phone = "";
  saleForm.customer_document = "";
  saleForm.customer_address = "";
}

function selectCustomer(customer) {
  saleForm.customer_id = customer.id;
  saleForm.customer_name = customer.nombre;
  saleForm.customer_phone = customer.telefono || "";
  saleForm.customer_document = customer.identificacion || "";
  saleForm.customer_address = customer.direccion || "";
  customerDialog.value = false;
}

function saveCustomer() {
  const nombre = (customerDraft.nombre || "").trim();
  if (!nombre) {
    showAlert("warning", "Ingresa el nombre del cliente para guardarlo.");
    return;
  }
  const customer = {
    id: Date.now(),
    nombre,
    telefono: (customerDraft.telefono || "").trim(),
    identificacion: (customerDraft.identificacion || "").trim(),
    direccion: (customerDraft.direccion || "").trim(),
  };
  customers.value.unshift(customer);
  selectCustomer(customer);
  customerDraft.nombre = "";
  customerDraft.telefono = "";
  customerDraft.identificacion = "";
  customerDraft.direccion = "";
  showCustomerCreate.value = false;
  showAlert("success", "Cliente agregado al flujo de venta.");
}

function saveVendor() {
  const nombre = (vendorDraft.nombre || "").trim();
  if (!nombre) {
    showAlert("warning", "Ingresa el nombre del vendedor.");
    return;
  }
  const vendor = { id: Date.now(), nombre };
  vendors.value.push(vendor);
  saleForm.vendedor_id = vendor.id;
  vendorDraft.nombre = "";
  vendorDialog.value = false;
  showAlert("success", "Vendedor agregado al flujo de ventas.");
}

function clearSale() {
  saleItems.value = [];
  payments.value = [];
  searchQuery.value = "";
  searchResults.value = [];
  searchActiveIndex.value = -1;
  saleForm.observacion = "";
  saleForm.condition = "CONTADO";
  saleForm.invoice_currency = "CS";
  saleForm.price_list = "1";
  paymentDraft.forma_id = "cash";
  paymentDraft.moneda = "CS";
  paymentDraft.monto = null;
  paymentDraft.banco_id = null;
  paymentDraft.cuenta_id = null;
  setDefaultCustomer();
  if (vendors.value.length) {
    saleForm.vendedor_id = vendors.value[0].id;
  }
  showAlert("success", "Venta limpiada. Lista para una nueva factura.");
}

function selectPaymentMethod(method) {
  paymentDraft.forma_id = method.id;
  if (!method.needsBank) {
    paymentDraft.banco_id = null;
    paymentDraft.cuenta_id = null;
  }
}

function addPayment() {
  if (saleForm.condition === "CREDITO") return;
  const method = paymentMethods.find((item) => item.id === paymentDraft.forma_id);
  const amount = Number(paymentDraft.monto || 0);
  if (!method || amount <= 0) {
    showAlert("warning", "Selecciona forma y monto valido.");
    return;
  }
  const bank = banks.find((item) => item.id === paymentDraft.banco_id);
  const account = accounts.find((item) => item.id === paymentDraft.cuenta_id);
  payments.value.push({
    id: `${method.id}-${Date.now()}`,
    forma_id: method.id,
    forma_label: method.label,
    moneda: paymentDraft.moneda,
    monto: amount,
    bank_label: bank?.nombre || "",
    cuenta_label: account?.label || "",
  });
  paymentDraft.monto = null;
  paymentDraft.banco_id = null;
  paymentDraft.cuenta_id = null;
}

function removePayment(paymentId) {
  payments.value = payments.value.filter((item) => item.id !== paymentId);
}

function fillRemainingAmount() {
  const remaining = paymentBalance.value;
  if (remaining <= 0) return;
  paymentDraft.moneda = saleForm.invoice_currency;
  paymentDraft.monto = Number(remaining.toFixed(2));
}

function openPaymentDialog() {
  if (!saleItems.value.length) {
    showAlert("warning", "Agrega al menos un producto antes de registrar la venta.");
    focusSearchInput();
    return;
  }
  currentTimeLabel.value = formatTimeNow();
  paymentDialog.value = true;
}

function confirmSale() {
  paymentDialog.value = false;
  showAlert("success", `Factura ${nextInvoice.value} preparada en la interfaz POS.`);
}

function showAlert(type, message) {
  salesAlert.type = type === "success" ? "success" : "warning";
  salesAlert.message = message;
  window.setTimeout(() => {
    if (salesAlert.message === message) {
      salesAlert.message = "";
    }
  }, 3200);
}

function setActiveTab(tab) {
  if (tab.disabled) {
    showAlert("warning", `${tab.label} aun no esta integrada en esta suite Vue.`);
    return;
  }
  activeTab.value = tab.key;
}

async function loadCatalogs() {
  const catalogData = await fetchInventoryCatalogs();
  catalogs.bodegas = catalogData.bodegas || [];
  if (!saleForm.bodega_id && catalogs.bodegas.length) {
    saleForm.bodega_id = catalogs.bodegas[0].id;
  }
}

async function loadBusinessSettings() {
  try {
    const settings = await fetchPublicBusinessSettings();
    businessSettings.sales_interface_code = settings.sales_interface_code || "ropa";
    if (settings.pricing_currency === "USD") {
      saleForm.invoice_currency = "USD";
      paymentDraft.moneda = "USD";
    }
  } catch {
    businessSettings.sales_interface_code = "ropa";
  }
}

function handleGlobalScanner(event) {
  const tagName = event.target?.tagName?.toLowerCase?.() || "";
  const isEditable = ["input", "textarea", "select"].includes(tagName);
  if (isEditable && event.target !== (searchInputRef.value?.$el?.querySelector?.("input") || searchInputRef.value)) {
    return;
  }

  if (event.key === "Enter") {
    const code = barcodeBuffer.value.trim();
    if (code.length >= 3) {
      lastScannedCode.value = code.toUpperCase();
      scannerState.value = "working";
      scannerLabel.value = "Escaneo recibido";
      searchQuery.value = code.toUpperCase();
      barcodeBuffer.value = "";
      return;
    }
  }

  if (event.key.length !== 1) return;
  if (/[\s]/.test(event.key)) return;

  barcodeBuffer.value += event.key.toUpperCase();
  if (barcodeResetTimer.value) clearTimeout(barcodeResetTimer.value);
  barcodeResetTimer.value = window.setTimeout(() => {
    barcodeBuffer.value = "";
    if (scannerState.value !== "error") {
      scannerState.value = "idle";
      scannerLabel.value = "Lector listo";
    }
  }, 120);
}

watch(
  () => searchQuery.value,
  () => {
    if (searchTimeout.value) clearTimeout(searchTimeout.value);
    const query = searchQuery.value.trim();
    if (query.length < 2) {
      searchResults.value = [];
      searchActiveIndex.value = -1;
      return;
    }
    searchTimeout.value = setTimeout(async () => {
      searchingProducts.value = true;
      try {
        const response = await searchInventoryProducts(query, saleForm.bodega_id || null, Number(saleForm.price_list || 1));
        searchResults.value = response.items || [];
        searchActiveIndex.value = searchResults.value.length ? 0 : -1;
        scannerState.value = searchResults.value.length ? "working" : "error";
        scannerLabel.value = searchResults.value.length ? "Lector listo" : "Sin coincidencias";
      } catch {
        searchResults.value = [];
        searchActiveIndex.value = -1;
        scannerState.value = "error";
        scannerLabel.value = "Error de busqueda";
      } finally {
        searchingProducts.value = false;
      }
    }, 160);
  },
);

watch(
  () => [saleForm.invoice_currency, saleForm.price_list],
  async () => {
    saleItems.value.forEach((item) => {
      item.precio = saleForm.invoice_currency === "USD"
        ? (item.subtotal_usd / Math.max(Number(item.cantidad || 1), 0.01))
        : (item.subtotal_cs / Math.max(Number(item.cantidad || 1), 0.01));
      recalculateItem(item);
    });
    paymentDraft.moneda = saleForm.invoice_currency;
    if (searchQuery.value.trim().length >= 2) {
      const response = await searchInventoryProducts(searchQuery.value.trim(), saleForm.bodega_id || null, Number(saleForm.price_list || 1));
      searchResults.value = response.items || [];
      searchActiveIndex.value = searchResults.value.length ? 0 : -1;
    }
  },
);

watch(
  () => saleForm.bodega_id,
  async () => {
    if (searchQuery.value.trim().length >= 2) {
      const response = await searchInventoryProducts(searchQuery.value.trim(), saleForm.bodega_id || null, Number(saleForm.price_list || 1));
      searchResults.value = response.items || [];
      searchActiveIndex.value = searchResults.value.length ? 0 : -1;
    }
  },
);

watch(
  () => saleForm.condition,
  (value) => {
    if (value === "CREDITO") {
      payments.value = [];
    }
  },
);

watch(
  () => paymentDraft.banco_id,
  () => {
    paymentDraft.cuenta_id = null;
  },
);

onMounted(async () => {
  await Promise.all([loadCatalogs(), loadBusinessSettings()]);
  if (vendors.value.length) {
    saleForm.vendedor_id = vendors.value[0].id;
  }
  setDefaultCustomer();
  focusSearchInput();
  window.addEventListener("keydown", handleGlobalScanner);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleGlobalScanner);
  if (searchTimeout.value) clearTimeout(searchTimeout.value);
  if (barcodeResetTimer.value) clearTimeout(barcodeResetTimer.value);
});
</script>
