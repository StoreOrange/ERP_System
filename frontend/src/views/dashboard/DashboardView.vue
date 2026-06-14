<template>
  <section class="page-section dashboard-page">
    <header class="dashboard-revamp-hero enterprise-dashboard-hero">
      <div class="dashboard-revamp-copy">
        <span class="dashboard-chip">Sistema empresarial</span>
        <h1>Panel principal de operacion</h1>
        <p>
          Un inicio para entrar rapido a productos, inventario, ventas y
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

    <div class="dashboard-kpi-strip enterprise-kpi-strip">
      <article class="dashboard-kpi-card dashboard-kpi-card-primary enterprise-kpi-card">
        <Skeleton v-if="loading" width="60%" height="1rem" />
        <template v-else>
          <span>Productos</span>
          <strong>{{ totals.products }}</strong>
          <small>Catalogo maestro cargado</small>
        </template>
      </article>
      <article class="dashboard-kpi-card enterprise-kpi-card">
        <span>Ingresos</span>
        <strong>{{ totals.ingresos }}</strong>
        <small>Movimientos de entrada</small>
        <Tag severity="success" value="Inventario +" rounded />
      </article>
      <article class="dashboard-kpi-card enterprise-kpi-card">
        <span>Egresos</span>
        <strong>{{ totals.egresos }}</strong>
        <small>Movimientos de salida</small>
        <Tag severity="warn" value="Inventario -" rounded />
      </article>
      <article class="dashboard-kpi-card enterprise-kpi-card">
        <span>Gestion financiera</span>
        <strong>C$ {{ formatMoney(financialBalance) }}</strong>
        <ProgressBar :value="implementationProgress" :show-value="false" />
        <small>Balance operativo estimado</small>
      </article>
    </div>

    <div class="enterprise-widget-grid">
      <Card class="executive-card enterprise-chart-card">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Indicadores</span>
              <h3>Ingresos vs egresos</h3>
            </div>
            <Tag severity="info" value="Tiempo real" rounded />
          </div>
        </template>
        <template #content>
          <VueApexCharts type="area" height="260" :options="movementChartOptions" :series="movementChartSeries" />
        </template>
      </Card>

      <Card class="executive-card enterprise-chart-card">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Inventario</span>
              <h3>Distribucion operativa</h3>
            </div>
          </div>
        </template>
        <template #content>
          <VueApexCharts type="donut" height="260" :options="inventoryChartOptions" :series="inventoryChartSeries" />
        </template>
      </Card>

      <Card class="executive-card enterprise-timeline-card">
        <template #title>
          <div class="dashboard-card-head">
            <div>
              <span class="products-section-kicker">Actividad</span>
              <h3>Linea operativa</h3>
            </div>
          </div>
        </template>
        <template #content>
          <Timeline :value="timelineItems" class="enterprise-timeline">
            <template #marker="{ item }">
              <span class="enterprise-timeline-marker" :class="item.status"></span>
            </template>
            <template #content="{ item }">
              <strong>{{ item.title }}</strong>
              <p>{{ item.detail }}</p>
            </template>
          </Timeline>
        </template>
      </Card>
    </div>

    <div class="dashboard-board enterprise-dashboard-board">
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
              <span class="module-status-dot ok"></span>
              <div>
                <strong>Facturacion POS activa</strong>
                <p>Ventas, pagos y descuento de inventario conectados.</p>
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
import { computed, onMounted, reactive, ref } from "vue";
import { RouterLink } from "vue-router";
import Button from "primevue/button";
import Card from "primevue/card";
import ProgressBar from "primevue/progressbar";
import Skeleton from "primevue/skeleton";
import Tag from "primevue/tag";
import Timeline from "primevue/timeline";
import VueApexCharts from "vue3-apexcharts";

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
const loading = ref(true);
const implementationProgress = 76;
const financialBalance = computed(() => (totals.ingresos - totals.egresos) * 1250);
const movementChartSeries = computed(() => [
  { name: "Ingresos", data: [0, totals.ingresos, Math.max(totals.ingresos + 2, 3), totals.ingresos + totals.products] },
  { name: "Egresos", data: [0, totals.egresos, Math.max(totals.egresos + 1, 2), totals.egresos + Math.round(totals.products / 3)] },
]);
const movementChartOptions = computed(() => ({
  chart: { toolbar: { show: false }, fontFamily: "inherit", sparkline: { enabled: false } },
  colors: ["#7557a8", "#d99058"],
  dataLabels: { enabled: false },
  stroke: { curve: "smooth", width: 3 },
  fill: { type: "gradient", gradient: { opacityFrom: 0.24, opacityTo: 0.02 } },
  grid: { borderColor: "#ede7f3", strokeDashArray: 4 },
  xaxis: { categories: ["Inicio", "Actual", "Proy.", "Total"], labels: { style: { colors: "#736b7f" } } },
  yaxis: { labels: { style: { colors: "#736b7f" } } },
  tooltip: { theme: "light" },
}));
const inventoryChartSeries = computed(() => [
  Math.max(totals.products, 1),
  Math.max(totals.ingresos, 1),
  Math.max(totals.egresos, 1),
]);
const inventoryChartOptions = computed(() => ({
  labels: ["Productos", "Ingresos", "Egresos"],
  chart: { fontFamily: "inherit" },
  colors: ["#7557a8", "#3d7a5b", "#a8723d"],
  legend: { position: "bottom", labels: { colors: "#736b7f" } },
  dataLabels: { enabled: false },
  stroke: { width: 0 },
  plotOptions: { pie: { donut: { size: "68%" } } },
}));
const timelineItems = computed(() => [
  { status: "ok", title: "Productos", detail: `${totals.products} registros disponibles para operacion.` },
  { status: "ok", title: "Inventario", detail: `${totals.ingresos + totals.egresos} movimientos registrados.` },
  { status: "warn", title: "Finanzas", detail: "Indicadores preparados para caja, bancos y cuentas." },
]);

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
  loading.value = true;
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
  } finally {
    loading.value = false;
  }
});

function formatMoney(value) {
  return new Intl.NumberFormat("es-NI", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value || 0));
}
</script>
