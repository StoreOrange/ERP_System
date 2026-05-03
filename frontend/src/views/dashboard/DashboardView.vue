<template>
  <section class="page-section dashboard-page">
    <header class="dashboard-revamp-hero">
      <div class="dashboard-revamp-copy">
        <span class="dashboard-chip">ERP Control Center</span>
        <h1>Panel principal de operacion</h1>
        <p>
          Un inicio tipo ERP para entrar rapido a productos, inventario, ventas y
          administracion, con resumen operativo y estado de implementacion.
        </p>
        <div class="dashboard-revamp-actions">
          <RouterLink to="/app/products" class="hero-link">
            <Button label="Abrir productos" severity="contrast" />
          </RouterLink>
          <RouterLink to="/app/inventory/movements" class="hero-link">
            <Button label="Abrir inventario" variant="outlined" />
          </RouterLink>
        </div>
      </div>

      <div class="dashboard-revamp-brief">
        <div class="dashboard-brief-card">
          <span>Fecha</span>
          <strong>{{ todayLabel }}</strong>
        </div>
        <div class="dashboard-brief-card">
          <span>Perfil</span>
          <strong>{{ currentRole }}</strong>
        </div>
        <div class="dashboard-brief-card">
          <span>Modulo siguiente</span>
          <strong>Ventas y facturacion</strong>
        </div>
      </div>
    </header>

    <div class="dashboard-kpi-strip">
      <article class="dashboard-kpi-card dashboard-kpi-card-primary">
        <span>Productos</span>
        <strong>{{ totals.products }}</strong>
        <small>Catalogo maestro cargado</small>
      </article>
      <article class="dashboard-kpi-card">
        <span>Ingresos</span>
        <strong>{{ totals.ingresos }}</strong>
        <small>Movimientos de entrada</small>
      </article>
      <article class="dashboard-kpi-card">
        <span>Egresos</span>
        <strong>{{ totals.egresos }}</strong>
        <small>Movimientos de salida</small>
      </article>
      <article class="dashboard-kpi-card">
        <span>Implementacion</span>
        <strong>64%</strong>
        <ProgressBar :value="64" :show-value="false" />
        <small>Core base listo, POS pendiente</small>
      </article>
    </div>

    <div class="dashboard-board">
      <Card class="executive-card dashboard-board-card dashboard-board-main">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Navegacion ejecutiva</span>
              <h3>Aplicaciones</h3>
            </div>
          </div>
        </template>
        <template #content>
          <div class="dashboard-module-grid">
            <RouterLink
              v-for="item in quickLinks"
              :key="item.route"
              :to="item.route"
              class="dashboard-module-tile"
            >
              <div class="dashboard-module-icon">
                <i class="bi" :class="item.icon"></i>
              </div>
              <div class="dashboard-module-copy">
                <strong>{{ item.label }}</strong>
                <span>Entrar al modulo</span>
              </div>
            </RouterLink>
          </div>
        </template>
      </Card>

      <Card class="executive-card dashboard-board-card">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Monitoreo</span>
              <h3>Estado del sistema</h3>
            </div>
          </div>
        </template>
        <template #content>
          <div class="dashboard-status-list">
            <div class="dashboard-status-row">
              <span class="module-status-dot ok"></span>
              <div>
                <strong>Inventario conectado</strong>
                <p>Productos y movimientos con backend funcional.</p>
              </div>
            </div>
            <div class="dashboard-status-row">
              <span class="module-status-dot ok"></span>
              <div>
                <strong>UI modular activa</strong>
                <p>Shell, dashboard y vistas base alineadas.</p>
              </div>
            </div>
            <div class="dashboard-status-row">
              <span class="module-status-dot warn"></span>
              <div>
                <strong>Facturacion pendiente</strong>
                <p>Falta caja, cobros, modal de pago y factura.</p>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <Card class="executive-card dashboard-board-card">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Plan inmediato</span>
              <h3>Ruta siguiente</h3>
            </div>
          </div>
        </template>
        <template #content>
          <ol class="dashboard-roadmap-list">
            <li>
              <strong>POS y cobro</strong>
              <span>Buscador comercial, carrito, pago y cierre de venta.</span>
            </li>
            <li>
              <strong>Inventario operativo</strong>
              <span>Formularios completos y control de bodega.</span>
            </li>
            <li>
              <strong>Seguridad</strong>
              <span>Usuarios, roles y permisos por modulo.</span>
            </li>
          </ol>
        </template>
      </Card>

      <Card class="executive-card dashboard-board-card dashboard-board-wide">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Resumen directivo</span>
              <h3>Panorama general</h3>
            </div>
          </div>
        </template>
        <template #content>
          <div class="dashboard-summary-grid">
            <div class="dashboard-summary-tile">
              <span>Operacion</span>
              <strong>Base navegable y funcional</strong>
              <small>Las aplicaciones principales ya son accesibles desde el shell.</small>
            </div>
            <div class="dashboard-summary-tile">
              <span>Inventario</span>
              <strong>Modelo espejo en progreso</strong>
              <small>La logica se sigue portando desde el sistema fuente.</small>
            </div>
            <div class="dashboard-summary-tile">
              <span>Siguiente frente</span>
              <strong>Ventas estilo Odoo</strong>
              <small>Facturacion, pagos y flujo completo de caja.</small>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive } from "vue";
import { RouterLink } from "vue-router";
import Button from "primevue/button";
import Card from "primevue/card";
import ProgressBar from "primevue/progressbar";

import { appNavigation } from "../../data/navigation";
import { readStoredUser } from "../../services/auth";
import { fetchEgresos, fetchIngresos, fetchProducts } from "../../services/inventory";

const quickLinks = appNavigation.filter((item) => item.route !== "/app/dashboard");
const currentUser = readStoredUser();

const totals = reactive({
  products: 0,
  ingresos: 0,
  egresos: 0,
});

const todayLabel = computed(() => {
  return new Intl.DateTimeFormat("es-NI", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  }).format(new Date());
});

const currentRole = computed(() => {
  const roles = currentUser?.roles || [];
  return roles.length ? roles[0].name : "Sesion principal";
});

onMounted(async () => {
  try {
    const [products, ingresos, egresos] = await Promise.all([
      fetchProducts(),
      fetchIngresos(),
      fetchEgresos(),
    ]);

    totals.products = products.length;
    totals.ingresos = ingresos.length;
    totals.egresos = egresos.length;
  } catch {
    totals.products = 0;
    totals.ingresos = 0;
    totals.egresos = 0;
  }
});
</script>
