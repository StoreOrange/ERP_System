<template>
  <section class="page-section sales-page" :class="salesInterfaceClass">
    <header class="sales-header-shell panel-card">
      <div class="sales-header-top">
        <div class="sales-header-copy">
          <p class="page-kicker">Punto de venta</p>
          <h1 class="page-title">{{ salesInterfaceTitle }}</h1>
          <p class="sales-interface-caption">{{ salesInterfaceCaption }}</p>
        </div>

        <div class="sales-kpi-grid">
          <article class="sales-kpi-box">
            <span>Factura</span>
            <strong>{{ nextInvoice }}</strong>
          </article>
          <article class="sales-kpi-box">
            <span>Bodega</span>
            <strong>{{ currentBodegaLabel }}</strong>
          </article>
          <article class="sales-kpi-box accent">
            <span>Total</span>
            <strong>{{ invoiceCurrencySymbol }} {{ formatMoney(invoiceTotal) }}</strong>
          </article>
        </div>
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
                <h3>Ticket actual</h3>
              </div>
              <Tag severity="contrast" :value="`${saleItems.length} productos`" rounded />
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

                    <div class="sales-ticket-readonly">
                      <span><b>Cant.</b> {{ formatQty(item.cantidad) }}</span>
                      <span><b>Precio</b> {{ invoiceCurrencySymbol }} {{ formatMoney(item.precio) }}</span>
                      <span><b>Stock</b> {{ formatQty(item.existencia) }}</span>
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
              <div class="sales-summary-chip sales-summary-total">
                <span>Total factura</span>
                <strong>{{ invoiceCurrencySymbol }} {{ formatMoney(invoiceTotal) }}</strong>
              </div>
              <div class="sales-summary-chip">
                <span>Unidades</span>
                <strong>{{ totalItems }}</strong>
              </div>
              <div class="sales-summary-chip">
                <span>Tasa</span>
                <strong>{{ hasExchangeRate ? `C$ ${formatRate(rateToday)}` : "Sin tasa" }}</strong>
              </div>
            </div>
            </div>
          </section>

          <section class="panel-card sales-card sales-invoice-card">
            <div class="sales-card-head">
              <div>
                <h3>Informacion de la factura</h3>
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
                  </div>
                </label>
              </div>

              <div class="field-group sales-date-field">
                <span>Fecha</span>
                <div ref="saleDatePickerRef" class="sales-date-control" :class="{ open: saleDatePickerOpen }">
                  <span class="sales-date-icon" aria-hidden="true">
                    <i class="bi bi-calendar3"></i>
                  </span>
                  <button type="button" class="sales-date-display" @click="toggleSaleDatePicker">
                    <strong>{{ formattedSaleDate }}</strong>
                  </button>

                  <div v-if="saleDatePickerOpen" class="sales-date-picker" role="dialog" aria-label="Seleccionar fecha">
                    <div class="sales-date-picker-head">
                      <button type="button" aria-label="Mes anterior" @click="moveSaleDateMonth(-1)">
                        <i class="bi bi-chevron-left"></i>
                      </button>
                      <strong>{{ saleDateMonthLabel }}</strong>
                      <button type="button" aria-label="Mes siguiente" @click="moveSaleDateMonth(1)">
                        <i class="bi bi-chevron-right"></i>
                      </button>
                    </div>
                    <div class="sales-date-weekdays">
                      <span v-for="day in saleDateWeekdays" :key="day">{{ day }}</span>
                    </div>
                    <div class="sales-date-days">
                      <button
                        v-for="day in saleDateCalendarDays"
                        :key="day.key"
                        type="button"
                        :class="{ muted: !day.currentMonth, today: day.isToday, selected: day.isSelected }"
                        @click="selectSaleDate(day.iso)"
                      >
                        {{ day.day }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>

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
                  <h3>Buscar productos</h3>
                </div>

                <div class="sales-search-meta">
                  <span class="scanner-badge" :class="scannerState">
                    <i class="bi bi-upc-scan"></i>
                    {{ scannerLabel }}
                  </span>
                  <span v-if="lastScannedCode" class="scanner-last">Ultimo: {{ lastScannedCode }}</span>
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

            <div
              ref="searchPanelRef"
              class="sales-search-panel"
              :class="`sales-search-panel-${salesInterfaceCode}`"
              tabindex="0"
              role="listbox"
              aria-label="Resultados de productos"
            >
              <div class="sales-search-head">
                <span>Producto</span>
                <span>Cargar</span>
              </div>

              <div v-if="searchingProducts" class="empty-state">Buscando productos...</div>
              <template v-else-if="searchQuery.trim().length < 2"></template>
              <div v-else-if="searchResults.length === 0" class="empty-state">Sin resultados para esta busqueda.</div>

              <div v-else-if="salesInterfaceCode === 'supermarket'" class="sales-product-grid">
                <article
                  v-for="(item, index) in searchResults"
                  :key="item.id"
                  class="sales-product-tile sales-search-item"
                  :class="{ active: searchActiveIndex === index, stockout: !hasProductStock(item) }"
                >
                  <span class="sales-product-code">{{ item.cod_producto }}</span>
                  <strong>{{ item.descripcion }}</strong>
                  <small>Stock {{ formatQty(item.existencia) }}</small>
                  <span class="sales-product-price">{{ invoiceCurrencySymbol }} {{ formatMoney(resolvePrice(item)) }}</span>
                  <div class="sales-search-qty">
                    <button type="button" :disabled="!canDecreaseSearchQty(item)" @click="decreaseSearchQty(item)">-</button>
                    <strong>{{ formatQty(searchQuantity(item)) }}</strong>
                    <button type="button" :disabled="!canIncreaseSearchQty(item)" @click="increaseSearchQty(item)">+</button>
                  </div>
                  <Button
                    type="button"
                    size="small"
                    icon="bi bi-plus-lg"
                    label="Cargar"
                    :disabled="!canLoadSearchProduct(item)"
                    @click="addProductToSale(item)"
                  />
                </article>
              </div>

              <div v-else-if="salesInterfaceCode === 'hardware'" class="sales-hardware-results">
                <article
                  v-for="(item, index) in searchResults"
                  :key="item.id"
                  class="sales-hardware-row sales-search-item"
                  :class="{ active: searchActiveIndex === index, stockout: !hasProductStock(item) }"
                >
                  <span class="sales-hardware-code">{{ item.cod_producto }}</span>
                  <strong>{{ item.descripcion }}</strong>
                  <span>{{ item.codigo_barra || "SIN BARRA" }}</span>
                  <span>Stock {{ formatQty(item.existencia) }}</span>
                  <b>{{ invoiceCurrencySymbol }} {{ formatMoney(resolvePrice(item)) }}</b>
                  <div class="sales-search-qty">
                    <button type="button" :disabled="!canDecreaseSearchQty(item)" @click="decreaseSearchQty(item)">-</button>
                    <strong>{{ formatQty(searchQuantity(item)) }}</strong>
                    <button type="button" :disabled="!canIncreaseSearchQty(item)" @click="increaseSearchQty(item)">+</button>
                  </div>
                  <Button
                    type="button"
                    size="small"
                    icon="bi bi-plus-lg"
                    label="Cargar"
                    :disabled="!canLoadSearchProduct(item)"
                    @click="addProductToSale(item)"
                  />
                </article>
              </div>

              <div v-else class="sales-search-results">
                <article
                  v-for="(item, index) in searchResults"
                  :key="item.id"
                  class="sales-search-item"
                  :class="{ active: searchActiveIndex === index, stockout: !hasProductStock(item) }"
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
                  <div class="sales-search-qty">
                    <button type="button" :disabled="!canDecreaseSearchQty(item)" @click="decreaseSearchQty(item)">-</button>
                    <strong>{{ formatQty(searchQuantity(item)) }}</strong>
                    <button type="button" :disabled="!canIncreaseSearchQty(item)" @click="increaseSearchQty(item)">+</button>
                  </div>
                  <Button
                    type="button"
                    size="small"
                    icon="bi bi-plus-lg"
                    label="Cargar"
                    :disabled="!canLoadSearchProduct(item)"
                    @click="addProductToSale(item)"
                  />
                </article>
              </div>
            </div>
            </div>
          </section>
        </div>
      </div>
    </form>

    <Dialog
      v-model:visible="paymentDialog"
      modal
      :style="{ width: 'min(920px, 94vw)' }"
      class="sales-payment-dialog"
      @show="focusPaymentAmount"
    >
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
            <div class="sales-pay-row"><span>Fecha</span><strong>{{ formattedSaleDate }}</strong></div>
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
          </div>

          <div class="sales-pay-balance">
            <div class="sales-pay-row"><span>Total venta</span><strong>{{ invoiceCurrencySymbol }} {{ formatMoney(invoiceTotal) }}</strong></div>
            <div class="sales-pay-row"><span>Pagado</span><strong>{{ invoiceCurrencySymbol }} {{ formatMoney(totalPaidInInvoiceCurrency) }}</strong></div>
            <div class="sales-pay-row"><span>Saldo</span><strong :class="paymentBalance <= 0 ? 'balance-positive' : 'balance-negative'">{{ invoiceCurrencySymbol }} {{ formatMoney(Math.max(paymentBalance, 0)) }}</strong></div>
            <div class="sales-pay-row"><span>Vuelto</span><strong class="balance-positive">{{ invoiceCurrencySymbol }} {{ formatMoney(paymentChange) }}</strong></div>
          </div>
          </div>
        </section>

        <section class="panel-card sales-payment-card">
          <div class="sales-card-head">
            <div>
              <span class="products-section-kicker">Pago rapido</span>
              <h3>Aplicar pago</h3>
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

          <div v-if="saleForm.condition !== 'CREDITO'" class="sales-payment-formgrid payment-grid-wide sales-payment-entry-grid">
            <label class="field-group sales-payment-currency-field">
              <span>Moneda</span>
              <select v-model="paymentDraft.moneda" class="form-control">
                <option value="CS">C$</option>
                <option value="USD">USD</option>
              </select>
            </label>
            <label class="field-group sales-payment-amount-field">
              <span>Monto</span>
              <InputNumber
                ref="paymentAmountRef"
                v-model="paymentDraft.monto"
                :min="0"
                :min-fraction-digits="2"
                :max-fraction-digits="2"
                input-class="erp-number-input sales-payment-amount-input"
                @keydown.enter.prevent="handlePaymentEnter"
              />
            </label>
            <label v-if="showBankFields" class="field-group sales-payment-bank-field">
              <span>Banco</span>
              <Select
                v-model="paymentDraft.banco_id"
                :options="banks"
                option-label="nombre"
                option-value="id"
                placeholder="Selecciona"
              />
            </label>
            <label v-if="showBankFields" class="field-group sales-payment-account-field">
              <span>Cuenta</span>
              <Select
                v-model="paymentDraft.cuenta_id"
                :options="filteredAccounts"
                option-label="label"
                option-value="id"
                placeholder="Selecciona"
              />
            </label>
            <label class="field-group sales-payment-ref-field">
              <span>Referencia</span>
              <input
                v-model="paymentDraft.referencia"
                class="form-control"
                placeholder="Recibo, voucher o nota"
                @keydown.enter.prevent="handlePaymentEnter"
              />
            </label>
          </div>

          <div v-if="saleForm.condition !== 'CREDITO'" class="sales-payment-actions">
            <Button type="button" severity="secondary" variant="outlined" icon="bi bi-calculator" label="Completar saldo" @click="fillRemainingAmount" />
            <Button type="button" icon="bi bi-plus-lg" label="Agregar pago" @click="addPaymentAndRefocus" />
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
                  <span>{{ payment.moneda }} &middot; {{ payment.bank_label || "Sin banco" }} <template v-if="payment.cuenta_label">&middot; {{ payment.cuenta_label }}</template></span>
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
          <Button
            type="button"
            icon="bi bi-check2-circle"
            :label="saleSubmitting ? 'Registrando...' : 'Confirmar y registrar factura'"
            :disabled="saleSubmitting"
            @click="confirmSale"
          />
        </div>
      </template>
    </Dialog>

    <Dialog v-model:visible="receiptDialog" modal :style="{ width: 'min(420px, 94vw)' }" class="sales-receipt-dialog">
      <template #header>
        <div class="sales-payment-title">
          <span class="products-section-kicker">Factura POS</span>
          <h3>{{ lastInvoice?.invoice_number || "Factura" }}</h3>
        </div>
      </template>

      <article v-if="lastInvoice" class="pos-receipt">
        <header class="pos-receipt-head">
          <img v-if="businessInvoiceLogo" :src="businessInvoiceLogo" :alt="businessSettings.trade_name || 'Logo'" class="pos-receipt-logo" />
          <strong>{{ businessSettings.trade_name || "Orange Tec" }}</strong>
          <span>{{ businessSettings.legal_name || businessSettings.trade_name || "Sistema empresarial" }}</span>
          <small v-if="businessSettings.ruc">RUC: {{ businessSettings.ruc }}</small>
          <small v-if="businessSettings.address">{{ businessSettings.address }}</small>
          <small v-if="businessPhones">Tel: {{ businessPhones }}</small>
          <small v-if="businessSettings.email">{{ businessSettings.email }}</small>
          <small v-if="businessSettings.website">{{ businessSettings.website }}</small>
          <small>Factura: {{ lastInvoice.invoice_number }}</small>
          <small>Fecha: {{ formatDisplayDate(lastInvoice.fecha) }} &middot; {{ currentTimeLabel }}</small>
        </header>

        <section class="pos-receipt-party">
          <div><span>Cliente</span><strong>{{ lastInvoice.customer_name }}</strong></div>
          <div><span>Condicion</span><strong>{{ lastInvoice.condicion }}</strong></div>
          <div><span>Vendedor</span><strong>{{ lastInvoice.vendor_name || "-" }}</strong></div>
        </section>

        <section class="pos-receipt-lines">
          <div v-for="item in lastInvoice.items" :key="item.id" class="pos-receipt-line">
            <div>
              <strong>{{ item.descripcion }}</strong>
              <span>{{ item.cod_producto }} &middot; {{ formatQty(item.cantidad) }} {{ item.unidad || "UND" }}</span>
            </div>
            <b>{{ lastInvoice.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(lastInvoice.moneda === "USD" ? item.subtotal_usd : item.subtotal_cs) }}</b>
          </div>
        </section>

        <section class="pos-receipt-totals">
          <div><span>Total</span><strong>{{ lastInvoice.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(receiptTotal) }}</strong></div>
          <div><span>Pagado</span><strong>{{ lastInvoice.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(receiptPaid) }}</strong></div>
          <div v-if="receiptBalance > 0"><span>Saldo</span><strong>{{ lastInvoice.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(receiptBalance) }}</strong></div>
          <div v-if="receiptChange > 0"><span>Vuelto</span><strong>{{ lastInvoice.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(receiptChange) }}</strong></div>
        </section>

        <section class="pos-receipt-payments">
          <h4>Pagos</h4>
          <div v-if="!lastInvoice.payments?.length">Venta a credito / sin pagos aplicados.</div>
          <div v-for="payment in lastInvoice.payments" :key="payment.id">
            <span>{{ payment.forma_nombre }} {{ payment.banco ? `- ${payment.banco}` : "" }}</span>
            <strong>{{ payment.moneda === "USD" ? "US$" : "C$" }} {{ formatMoney(payment.monto) }}</strong>
          </div>
        </section>

        <footer class="pos-receipt-footer">
          Gracias por su compra
        </footer>
      </article>

      <template #footer>
        <div class="sales-payment-footer">
          <Button type="button" severity="secondary" variant="outlined" label="Cerrar" @click="receiptDialog = false" />
          <Button type="button" icon="bi bi-printer" label="Imprimir" @click="printReceipt" />
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
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

import { fetchVendors } from "../../services/access";
import { readStoredUser } from "../../services/auth";
import { fetchInventoryCatalogs, searchInventoryProducts } from "../../services/inventory";
import { createCustomer, createSalesInvoice, fetchCustomers, fetchNextSalesInvoice } from "../../services/sales";
import { buildAssetUrl, fetchCurrentExchangeRate, fetchPublicBusinessSettings } from "../../services/settings";

const currentUser = readStoredUser();
const paymentDialog = ref(false);
const receiptDialog = ref(false);
const saleSubmitting = ref(false);
const customerDialog = ref(false);
const searchingProducts = ref(false);
const showCustomerCreate = ref(false);
const searchQuery = ref("");
const searchResults = ref([]);
const searchActiveIndex = ref(-1);
const searchTimeout = ref(null);
const searchInputRef = ref(null);
const searchPanelRef = ref(null);
const paymentAmountRef = ref(null);
const saleDatePickerRef = ref(null);
const saleDatePickerOpen = ref(false);
const saleDateViewDate = ref(new Date());
const currentTimeLabel = ref(formatTimeNow());
const rateToday = ref(null);
const scannerState = ref("idle");
const scannerLabel = ref("Lector listo");
const lastScannedCode = ref("");
const barcodeBuffer = ref("");
const barcodeResetTimer = ref(null);
const catalogs = reactive({ bodegas: [], egreso_tipos: [] });
const businessSettings = reactive({
  sales_interface_code: "ecommerce",
  trade_name: "Orange Tec",
  legal_name: "Orange Tec",
  ruc: "",
  address: "",
  phone: "",
  phones: "",
  email: "",
  website: "",
  logo_invoice: "",
  logo_sidebar: "",
});
const saleItems = ref([]);
const payments = ref([]);
const searchQuantities = reactive({});
const backendNextInvoice = ref("POS-000001");
const lastInvoice = ref(null);
const salesAlert = reactive({ type: "success", message: "" });
const customerSearch = ref("");
const DEFAULT_PRICE_LIST = 1;
const confirm = useConfirm();
const toast = useToast();

const saleForm = reactive({
  customer_id: null,
  customer_name: "Consumidor final",
  customer_phone: "",
  customer_document: "",
  customer_address: "",
  vendedor_id: null,
  date: todayIsoDate(),
  condition: "CONTADO",
  observacion: "",
  bodega_id: null,
  invoice_currency: "CS",
});

const customerDraft = reactive({
  nombre: "",
  telefono: "",
  identificacion: "",
  direccion: "",
});

const customers = ref([
  { id: 1, nombre: "Consumidor final", telefono: "", identificacion: "", direccion: "" },
]);

const vendors = ref([
  { id: 1, nombre: "Vendedor de piso" },
]);

const paymentDraft = reactive({
  forma_id: "cash",
  moneda: "CS",
  monto: null,
  banco_id: null,
  cuenta_id: null,
  referencia: "",
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

const nextInvoice = computed(() => backendNextInvoice.value || "POS-000001");
const hasExchangeRate = computed(() => Number(rateToday.value || 0) > 0);
const invoiceCurrencySymbol = computed(() => (saleForm.invoice_currency === "USD" ? "US$" : "C$"));
const currentBodegaLabel = computed(() => {
  const bodega = catalogs.bodegas.find((item) => item.id === saleForm.bodega_id);
  return bodega?.name || "-";
});
const totalUsd = computed(() => saleItems.value.reduce((sum, item) => sum + Number(item.subtotal_usd || 0), 0));
const totalCs = computed(() => saleItems.value.reduce((sum, item) => sum + Number(item.subtotal_cs || 0), 0));
const invoiceTotal = computed(() => (saleForm.invoice_currency === "USD" ? totalUsd.value : totalCs.value));
const totalItems = computed(() => saleItems.value.reduce((sum, item) => sum + Number(item.cantidad || 0), 0).toFixed(2));
const selectedVendor = computed(() => vendors.value.find((item) => item.id === saleForm.vendedor_id) || null);
const selectedVendorName = computed(() => vendors.value.find((item) => item.id === saleForm.vendedor_id)?.nombre || "Vendedor");
const formattedSaleDate = computed(() => formatDisplayDate(saleForm.date));
const businessPhones = computed(() =>
  [businessSettings.phone, businessSettings.phones].filter(Boolean).join(" / "),
);
const businessInvoiceLogo = computed(() => buildAssetUrl(businessSettings.logo_invoice || businessSettings.logo_sidebar));
const saleDateWeekdays = ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"];
const saleDateMonthLabel = computed(() =>
  new Intl.DateTimeFormat("es-NI", {
    month: "long",
    year: "numeric",
  }).format(saleDateViewDate.value),
);
const saleDateCalendarDays = computed(() => buildSaleDateCalendar(saleDateViewDate.value, saleForm.date));
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
const paymentChange = computed(() => Math.max(totalPaidInInvoiceCurrency.value - invoiceTotal.value, 0));
const showBankFields = computed(() => paymentMethods.find((item) => item.id === paymentDraft.forma_id)?.needsBank || false);
const filteredAccounts = computed(() =>
  accounts.filter((item) => (!paymentDraft.banco_id || item.banco_id === paymentDraft.banco_id) && item.moneda === paymentDraft.moneda),
);
const receiptTotal = computed(() =>
  lastInvoice.value?.moneda === "USD"
    ? Number(lastInvoice.value?.total_usd || 0)
    : Number(lastInvoice.value?.total_cs || 0),
);
const receiptPaid = computed(() =>
  lastInvoice.value?.moneda === "USD"
    ? Number(lastInvoice.value?.paid_usd || 0)
    : Number(lastInvoice.value?.paid_cs || 0),
);
const receiptChange = computed(() =>
  lastInvoice.value?.moneda === "USD"
    ? Number(lastInvoice.value?.change_usd || 0)
    : Number(lastInvoice.value?.change_cs || 0),
);
const receiptBalance = computed(() =>
  lastInvoice.value?.moneda === "USD"
    ? Number(lastInvoice.value?.balance_usd || 0)
    : Number(lastInvoice.value?.balance_cs || 0),
);
const salesInterfaceMap = {
  ecommerce: {
    title: "Venta ecommerce",
    caption: "Interfaz de ventas para la facturacion al cliente.",
  },
  supermarket: {
    title: "Venta supermercado",
    caption: "Grilla rapida para buscar, tocar y cargar productos al ticket en el mismo panel.",
  },
  hardware: {
    title: "Venta ferreteria",
    caption: "Busqueda general por codigo, barra y descripcion con filas densas para mostrador.",
  },
};
const salesInterfaceCode = computed(() => {
  const code = String(businessSettings.sales_interface_code || "ecommerce").trim().toLowerCase();
  const legacyMap = {
    ropa: "ecommerce",
    zapatos: "ecommerce",
    restaurante: "supermarket",
    comestibles: "supermarket",
    ferreteria: "hardware",
  };
  const normalized = legacyMap[code] || code;
  return salesInterfaceMap[normalized] ? normalized : "ecommerce";
});
const salesInterfaceTitle = computed(() => salesInterfaceMap[salesInterfaceCode.value].title);
const salesInterfaceCaption = computed(() => salesInterfaceMap[salesInterfaceCode.value].caption);
const salesInterfaceClass = computed(() => `sales-interface-${salesInterfaceCode.value}`);
const filteredCustomers = computed(() => {
  const query = customerSearch.value.trim().toLowerCase();
  if (!query) return customers.value;
  return customers.value.filter((item) =>
    [item.nombre, item.identificacion, item.telefono].some((value) => String(value || "").toLowerCase().includes(query)),
  );
});

function getRate() {
  return Number(rateToday.value || 0);
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

function todayIsoDate() {
  return toIsoDate(new Date());
}

function formatDisplayDate(value) {
  const date = parseIsoDate(value || todayIsoDate());
  return [
    String(date.getDate()).padStart(2, "0"),
    String(date.getMonth() + 1).padStart(2, "0"),
    date.getFullYear(),
  ].join("-");
}

function parseIsoDate(value) {
  const [year, month, day] = String(value || todayIsoDate()).split("-").map(Number);
  return new Date(year, month - 1, day || 1);
}

function toIsoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function buildSaleDateCalendar(viewDate, selectedIso) {
  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();
  const firstDay = new Date(year, month, 1);
  const start = new Date(year, month, 1 - firstDay.getDay());
  const today = todayIsoDate();
  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    const iso = toIsoDate(date);
    return {
      key: `${iso}-${index}`,
      iso,
      day: date.getDate(),
      currentMonth: date.getMonth() === month,
      isToday: iso === today,
      isSelected: iso === selectedIso,
    };
  });
}

function toggleSaleDatePicker() {
  saleDateViewDate.value = parseIsoDate(saleForm.date);
  saleDatePickerOpen.value = !saleDatePickerOpen.value;
}

function moveSaleDateMonth(direction) {
  const nextDate = new Date(saleDateViewDate.value);
  nextDate.setMonth(nextDate.getMonth() + direction);
  saleDateViewDate.value = nextDate;
}

function selectSaleDate(isoDate) {
  saleForm.date = isoDate;
  saleDateViewDate.value = parseIsoDate(isoDate);
  saleDatePickerOpen.value = false;
}

function handleSaleDateOutsideClick(event) {
  if (!saleDatePickerOpen.value) return;
  const root = saleDatePickerRef.value;
  if (root && !root.contains(event.target)) {
    saleDatePickerOpen.value = false;
  }
}

function resolvePrice(item) {
  const priceTier = DEFAULT_PRICE_LIST;
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

function stockQty(value) {
  return Number(Number(value || 0).toFixed(4));
}

function hasProductStock(product) {
  const minimumQty = product?.es_por_peso ? 0.01 : 1;
  return stockQty(product?.existencia ?? product?.free_qty) >= minimumQty;
}

function availableProductStock(productOrItem) {
  return stockQty(productOrItem?.existencia ?? productOrItem?.free_qty);
}

function productStepQty(product) {
  return product?.es_por_peso ? 0.01 : 1;
}

function searchQuantity(product) {
  const key = String(product?.id || "");
  const maxQty = maxSearchQuantity(product);
  if (maxQty <= 0) {
    searchQuantities[key] = 0;
    return 0;
  }
  const current = Number(searchQuantities[key] || 0);
  if (current > 0) {
    const clamped = Math.min(stockQty(current), maxQty);
    searchQuantities[key] = clamped;
    return clamped;
  }
  const initial = productStepQty(product);
  searchQuantities[key] = Math.min(initial, maxQty);
  return searchQuantities[key];
}

function maxSearchQuantity(product) {
  const productId = product?.product_id || product?.id;
  const available = availableProductStock(product);
  const reserved = reservedQuantityForProduct(productId);
  return Math.max(stockQty(available - reserved), 0);
}

function setSearchQuantity(product, quantity) {
  const key = String(product?.id || "");
  const step = productStepQty(product);
  const maxQty = maxSearchQuantity(product);
  if (maxQty <= 0) {
    searchQuantities[key] = 0;
    return;
  }
  const normalized = product?.es_por_peso
    ? stockQty(quantity)
    : Math.floor(Number(quantity || 0));
  searchQuantities[key] = Math.min(Math.max(normalized, step), maxQty);
}

function canDecreaseSearchQty(product) {
  return searchQuantity(product) > productStepQty(product);
}

function canIncreaseSearchQty(product) {
  return searchQuantity(product) < maxSearchQuantity(product);
}

function decreaseSearchQty(product) {
  setSearchQuantity(product, searchQuantity(product) - productStepQty(product));
}

function increaseSearchQty(product) {
  setSearchQuantity(product, searchQuantity(product) + productStepQty(product));
}

function canLoadSearchProduct(product) {
  return validateProductQuantity(product, searchQuantity(product)).ok;
}

function reservedQuantityForProduct(productId, excludeItemId = null) {
  return stockQty(
    saleItems.value.reduce((sum, item) => {
      if (item.product_id !== productId || item.id === excludeItemId) return sum;
      return sum + Number(item.cantidad || 0);
    }, 0),
  );
}

function validateProductQuantity(productOrItem, requestedQty, excludeItemId = null) {
  const productId = productOrItem.product_id || productOrItem.id;
  const available = availableProductStock(productOrItem);
  const reserved = reservedQuantityForProduct(productId, excludeItemId);
  const requested = stockQty(requestedQty);
  const remaining = stockQty(available - reserved);

  if (available <= 0) {
    return {
      ok: false,
      allowed: 0,
      message: `${productOrItem.cod_producto || "Producto"} sin existencia disponible.`,
    };
  }

  if (requested > remaining) {
    return {
      ok: false,
      allowed: Math.max(remaining, 0),
      message: `Stock insuficiente para ${productOrItem.cod_producto}. Disponible: ${formatQty(Math.max(remaining, 0))}.`,
    };
  }

  return { ok: true, allowed: requested };
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

function normalizeProductForSale(product, quantity = null) {
  const price = resolvePrice(product);
  const qty = quantity ?? productStepQty(product);
  const normalized = {
    id: `${product.id}-${Date.now()}-${Math.random().toString(16).slice(2, 6)}`,
    product_id: product.id,
    cod_producto: product.cod_producto,
    codigo_barra: product.codigo_barra,
    descripcion: product.descripcion,
    unidad_medida_abreviatura: product.unidad_medida_abreviatura || "UND",
    es_por_peso: Boolean(product.es_por_peso),
    existencia: availableProductStock(product),
    free_qty: availableProductStock(product),
    bodega_id: saleForm.bodega_id,
    cantidad: qty,
    precio: price,
    subtotal: 0,
    subtotal_usd: 0,
    subtotal_cs: 0,
  };
  recalculateItem(normalized);
  return normalized;
}

function addProductToSale(product, quantity = null) {
  const selectedQty = stockQty(quantity ?? searchQuantity(product));
  const validation = validateProductQuantity(product, selectedQty);
  if (!validation.ok) {
    showAlert("warning", validation.message);
    scannerState.value = "error";
    scannerLabel.value = "Sin stock";
    return;
  }

  const currentPrice = Number(resolvePrice(product));
  const existing = saleItems.value.find((item) => item.product_id === product.id && Number(item.precio || 0) === currentPrice);
  if (existing) {
    const nextQty = Number(existing.cantidad || 0) + selectedQty;
    const existingValidation = validateProductQuantity(existing, nextQty, existing.id);
    if (!existingValidation.ok) {
      showAlert("warning", existingValidation.message);
      scannerState.value = "error";
      scannerLabel.value = "Sin stock";
      return;
    }
    existing.cantidad = nextQty;
    recalculateItem(existing);
  } else {
    saleItems.value.push(normalizeProductForSale(product, selectedQty));
  }
  setSearchQuantity(product, productStepQty(product));
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

function validateSaleStock() {
  const problems = [];
  const grouped = new Map();

  saleItems.value.forEach((item) => {
    const current = grouped.get(item.product_id) || {
      cod_producto: item.cod_producto,
      existencia: availableProductStock(item),
      cantidad: 0,
    };
    current.cantidad += Number(item.cantidad || 0);
    grouped.set(item.product_id, current);
  });

  grouped.forEach((item) => {
    if (Number(item.cantidad || 0) <= 0) {
      problems.push(`${item.cod_producto}: cantidad invalida.`);
    } else if (stockQty(item.cantidad) > stockQty(item.existencia)) {
      problems.push(`${item.cod_producto}: solicitado ${formatQty(item.cantidad)}, disponible ${formatQty(item.existencia)}.`);
    }
  });

  return problems;
}

function removeSaleItem(itemId) {
  const item = saleItems.value.find((entry) => entry.id === itemId);
  confirm.require({
    header: "Quitar producto",
    message: `Confirma quitar ${item?.cod_producto || "este producto"} del ticket actual.`,
    icon: "bi bi-trash",
    rejectLabel: "Cancelar",
    acceptLabel: "Quitar",
    acceptClass: "p-button-danger",
    accept: () => {
      saleItems.value = saleItems.value.filter((entry) => entry.id !== itemId);
      showAlert("success", "Producto retirado del ticket.");
    },
  });
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

async function saveCustomer() {
  const nombre = (customerDraft.nombre || "").trim();
  if (!nombre) {
    showAlert("warning", "Ingresa el nombre del cliente para guardarlo.");
    return;
  }
  try {
    const customer = await createCustomer({
      nombre,
      telefono: (customerDraft.telefono || "").trim(),
      identificacion: (customerDraft.identificacion || "").trim(),
      direccion: (customerDraft.direccion || "").trim(),
      activo: true,
    });
    await loadCustomers();
    selectCustomer(customer);
    customerDraft.nombre = "";
    customerDraft.telefono = "";
    customerDraft.identificacion = "";
    customerDraft.direccion = "";
    showCustomerCreate.value = false;
    showAlert("success", "Cliente agregado al catalogo.");
  } catch (error) {
    showAlert("warning", error.message || "No se pudo guardar el cliente.");
  }
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
  paymentDraft.forma_id = "cash";
  paymentDraft.moneda = "CS";
  paymentDraft.monto = null;
  paymentDraft.banco_id = null;
  paymentDraft.cuenta_id = null;
  paymentDraft.referencia = "";
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
  focusPaymentAmount();
}

function addPayment() {
  if (saleForm.condition === "CREDITO") return false;
  const method = paymentMethods.find((item) => item.id === paymentDraft.forma_id);
  const amount = Number(paymentDraft.monto || 0);
  if (!method || amount <= 0) {
    showAlert("warning", "Selecciona forma y monto valido.");
    return false;
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
    referencia: (paymentDraft.referencia || "").trim(),
  });
  paymentDraft.monto = null;
  paymentDraft.banco_id = null;
  paymentDraft.cuenta_id = null;
  paymentDraft.referencia = "";
  return true;
}

function addPaymentAndRefocus() {
  const created = addPayment();
  focusPaymentAmount();
  return created;
}

async function handlePaymentEnter() {
  if (Number(paymentDraft.monto || 0) > 0) {
    addPaymentAndRefocus();
    return;
  }

  if (saleForm.condition !== "CREDITO" && payments.value.length && paymentBalance.value <= 0.009) {
    await confirmSale();
    return;
  }

  if (saleForm.condition !== "CREDITO" && paymentBalance.value > 0.009) {
    fillRemainingAmount();
    return;
  }

  focusPaymentAmount();
}

function removePayment(paymentId) {
  payments.value = payments.value.filter((item) => item.id !== paymentId);
}

function fillRemainingAmount() {
  const remaining = paymentBalance.value;
  if (remaining <= 0) return;
  paymentDraft.moneda = saleForm.invoice_currency;
  paymentDraft.monto = Number(remaining.toFixed(2));
  focusPaymentAmount();
}

function prepareDefaultPaymentAmount() {
  if (saleForm.condition === "CREDITO") return;
  const remaining = Math.max(Number(paymentBalance.value || 0), 0);
  paymentDraft.moneda = saleForm.invoice_currency;
  paymentDraft.monto = Number(remaining.toFixed(2));
}

function openPaymentDialog() {
  if (!saleItems.value.length) {
    showAlert("warning", "Agrega al menos un producto antes de registrar la venta.");
    focusSearchInput();
    return;
  }
  const stockProblems = validateSaleStock();
  if (stockProblems.length) {
    showAlert("warning", `Control de inventario: ${stockProblems[0]}`);
    return;
  }
  if (saleForm.invoice_currency === "USD" && !hasExchangeRate.value) {
    showAlert("warning", "Registra una tasa de cambio vigente antes de facturar en USD.");
    return;
  }
  currentTimeLabel.value = formatTimeNow();
  prepareDefaultPaymentAmount();
  paymentDialog.value = true;
  focusPaymentAmount();
}

function focusPaymentAmount() {
  nextTick(() => {
    const input =
      paymentAmountRef.value?.$el?.querySelector?.("input") ||
      paymentAmountRef.value?.input ||
      paymentAmountRef.value;
    input?.focus?.();
    input?.select?.();
  });
}

async function confirmSale() {
  const stockProblems = validateSaleStock();
  if (stockProblems.length) {
    showAlert("warning", `Control de inventario: ${stockProblems[0]}`);
    return;
  }

  if (saleForm.condition !== "CREDITO" && payments.value.length === 0) {
    showAlert("warning", "Agrega al menos una forma de pago para venta de contado.");
    return;
  }
  if (saleForm.condition !== "CREDITO" && paymentBalance.value > 0.009) {
    showAlert("warning", "El pago no cubre el total de la factura.");
    return;
  }

  saleSubmitting.value = true;
  try {
    const invoice = await createSalesInvoice({
      customer_name: saleForm.customer_name || "Consumidor final",
      customer_phone: saleForm.customer_phone || "",
      customer_document: saleForm.customer_document || "",
      customer_address: saleForm.customer_address || "",
      vendor_name: selectedVendorName.value,
      bodega_id: saleForm.bodega_id,
      fecha: saleForm.date,
      condicion: saleForm.condition,
      moneda: saleForm.invoice_currency,
      tasa_cambio: hasExchangeRate.value ? Number(rateToday.value) : null,
      observacion: saleForm.observacion || "",
      usuario_registro: currentUser?.email || currentUser?.full_name || "sistema",
      items: saleItems.value.map((item) => ({
        producto_id: item.product_id,
        cantidad: Number(item.cantidad || 0),
        precio_unitario: Number(item.precio || 0),
        cod_producto: item.cod_producto,
        descripcion: item.descripcion,
        unidad: item.unidad_medida_abreviatura || "UND",
      })),
      payments: saleForm.condition === "CREDITO"
        ? []
        : payments.value.map((payment) => ({
            forma_codigo: payment.forma_id,
            forma_nombre: payment.forma_label,
            moneda: payment.moneda,
            monto: Number(payment.monto || 0),
            banco: payment.bank_label || "",
            cuenta: payment.cuenta_label || "",
            referencia: payment.referencia || "",
          })),
    });
    lastInvoice.value = invoice;
    paymentDialog.value = false;
    clearSale();
    await loadNextInvoice();
    receiptDialog.value = true;
    showAlert("success", `${invoice.invoice_number} registrada, pagada y descontada del inventario.`);
  } catch (error) {
    showAlert("warning", error.message || "No se pudo registrar la factura POS.");
  } finally {
    saleSubmitting.value = false;
  }
}

function showAlert(type, message) {
  salesAlert.type = type === "success" ? "success" : "warning";
  salesAlert.message = message;
  toast.add({
    severity: type === "success" ? "success" : "warn",
    summary: type === "success" ? "Operacion realizada" : "Atencion",
    detail: message,
    life: type === "success" ? 2600 : 4200,
  });
  window.setTimeout(() => {
    if (salesAlert.message === message) {
      salesAlert.message = "";
    }
  }, 3200);
}

function printReceipt() {
  document.body.classList.add("printing-sales-receipt");
  window.print();
  window.setTimeout(() => {
    document.body.classList.remove("printing-sales-receipt");
  }, 500);
}

async function loadCatalogs() {
  const catalogData = await fetchInventoryCatalogs();
  catalogs.bodegas = catalogData.bodegas || [];
  catalogs.egreso_tipos = catalogData.egreso_tipos || [];
  if (!saleForm.bodega_id && catalogs.bodegas.length) {
    saleForm.bodega_id = defaultSalesBodegaId();
  }
}

function defaultSalesBodegaId() {
  const preferred = catalogs.bodegas.find((item) => /central/i.test(`${item.code || ""} ${item.name || ""}`));
  return preferred?.id || catalogs.bodegas[0]?.id || null;
}

function applyVendorBodega(vendor, { silent = false } = {}) {
  if (!vendor?.bodega_id || saleForm.bodega_id === vendor.bodega_id) return;
  if (isPrincipalBodega(vendor.bodega_id) && !silent) return;
  const exists = catalogs.bodegas.some((item) => item.id === vendor.bodega_id);
  if (!exists) return;
  saleForm.bodega_id = vendor.bodega_id;
  if (!silent) {
    showAlert("warning", "Bodega actualizada segun el vendedor seleccionado.");
  }
}

function isPrincipalBodega(bodegaId) {
  const bodega = catalogs.bodegas.find((item) => item.id === bodegaId);
  return /principal|bod-001/i.test(`${bodega?.code || ""} ${bodega?.name || ""}`);
}

async function loadVendors() {
  try {
    const response = await fetchVendors();
    const sorted = [...response].sort((a, b) => {
      const aFloor = /vendedor de piso/i.test(a.nombre || "");
      const bFloor = /vendedor de piso/i.test(b.nombre || "");
      if (aFloor && !bFloor) return -1;
      if (!aFloor && bFloor) return 1;
      return (a.nombre || "").localeCompare(b.nombre || "");
    });
    vendors.value = sorted.length
      ? sorted.map((vendor) => ({
          id: vendor.id,
          nombre: vendor.nombre,
          bodega_id: vendor.bodega_id,
          sucursal_id: vendor.sucursal_id,
          user_id: vendor.user_id,
        }))
      : vendors.value;
  } catch {
    vendors.value = vendors.value.length
      ? vendors.value
      : [{ id: 1, nombre: "Vendedor de piso" }];
  }
}

async function loadCustomers() {
  try {
    const response = await fetchCustomers();
    customers.value = [
      { id: 1, nombre: "Consumidor final", telefono: "", identificacion: "", direccion: "" },
      ...response.filter((customer) => !/consumidor final/i.test(customer.nombre || "")),
    ];
  } catch {
    customers.value = customers.value.length
      ? customers.value
      : [{ id: 1, nombre: "Consumidor final", telefono: "", identificacion: "", direccion: "" }];
  }
}

async function loadBusinessSettings() {
  try {
    const settings = await fetchPublicBusinessSettings();
    businessSettings.sales_interface_code = settings.sales_interface_code || "ecommerce";
    businessSettings.trade_name = settings.trade_name || settings.business_name || "Orange Tec";
    businessSettings.legal_name = settings.legal_name || businessSettings.trade_name;
    businessSettings.ruc = settings.ruc || "";
    businessSettings.address = settings.address || "";
    businessSettings.phone = settings.phone || "";
    businessSettings.phones = settings.phones || "";
    businessSettings.email = settings.email || "";
    businessSettings.website = settings.website || "";
    businessSettings.logo_invoice = settings.logo_invoice || "";
    businessSettings.logo_sidebar = settings.logo_sidebar || "";
    if (settings.pricing_currency === "USD") {
      saleForm.invoice_currency = "USD";
      paymentDraft.moneda = "USD";
    }
  } catch {
    businessSettings.sales_interface_code = "ecommerce";
  }
}

async function loadNextInvoice() {
  try {
    const response = await fetchNextSalesInvoice();
    backendNextInvoice.value = response.invoice_number || "POS-000001";
  } catch {
    backendNextInvoice.value = "POS-000001";
  }
}

async function loadCurrentExchangeRate() {
  try {
    const currentRate = await fetchCurrentExchangeRate();
    rateToday.value = currentRate?.rate ? Number(currentRate.rate) : null;
  } catch {
    rateToday.value = null;
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
        const response = await searchInventoryProducts(query, saleForm.bodega_id || null, 1);
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
  () => saleForm.invoice_currency,
  async () => {
    saleItems.value.forEach((item) => {
      item.precio = saleForm.invoice_currency === "USD"
        ? (item.subtotal_usd / Math.max(Number(item.cantidad || 1), 0.01))
        : (item.subtotal_cs / Math.max(Number(item.cantidad || 1), 0.01));
      recalculateItem(item);
    });
    paymentDraft.moneda = saleForm.invoice_currency;
    if (searchQuery.value.trim().length >= 2) {
      const response = await searchInventoryProducts(searchQuery.value.trim(), saleForm.bodega_id || null, 1);
      searchResults.value = response.items || [];
      searchActiveIndex.value = searchResults.value.length ? 0 : -1;
    }
  },
);

watch(
  () => saleForm.bodega_id,
  async (newBodegaId, oldBodegaId) => {
    if (oldBodegaId && newBodegaId !== oldBodegaId && saleItems.value.length) {
      saleItems.value = [];
      payments.value = [];
      showAlert("warning", "Ticket limpiado por cambio de bodega. La existencia se valida por bodega.");
    }
    if (searchQuery.value.trim().length >= 2) {
      const response = await searchInventoryProducts(searchQuery.value.trim(), saleForm.bodega_id || null, 1);
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
  await Promise.all([loadCatalogs(), loadVendors(), loadCustomers(), loadBusinessSettings(), loadCurrentExchangeRate(), loadNextInvoice()]);
  saleForm.bodega_id = defaultSalesBodegaId();
  if (vendors.value.length) {
    saleForm.vendedor_id = vendors.value[0].id;
    if (!isPrincipalBodega(vendors.value[0].bodega_id)) {
      applyVendorBodega(vendors.value[0], { silent: true });
    }
  }
  setDefaultCustomer();
  focusSearchInput();
  window.addEventListener("keydown", handleGlobalScanner);
  document.addEventListener("mousedown", handleSaleDateOutsideClick);
});

watch(
  () => saleForm.vendedor_id,
  (vendorId, previousVendorId) => {
    if (!vendorId || vendorId === previousVendorId) return;
    applyVendorBodega(selectedVendor.value);
  },
);

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleGlobalScanner);
  document.removeEventListener("mousedown", handleSaleDateOutsideClick);
  if (searchTimeout.value) clearTimeout(searchTimeout.value);
  if (barcodeResetTimer.value) clearTimeout(barcodeResetTimer.value);
});
</script>
