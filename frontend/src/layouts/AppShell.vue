<template>
  <div :class="['app-shell', { 'sidebar-collapsed': collapsed }]">
    <aside :class="['app-sidebar', { collapsed }]">
      <div class="sidebar-top">
        <div class="brand-wrap" v-if="!collapsed">
          <div class="brand-logo-shell" v-if="businessSettings.logo_sidebar">
            <img :src="buildAssetUrl(businessSettings.logo_sidebar)" :alt="businessLabel" />
          </div>
          <p class="brand-kicker">ERP Empresarial</p>
          <h1 class="brand-name">{{ businessLabel }}</h1>
          <p v-if="businessSettings.sidebar_subtitle" class="brand-caption">{{ businessSettings.sidebar_subtitle }}</p>
        </div>
        <button class="sidebar-toggle" type="button" @click="collapsed = !collapsed">
          <i class="bi" :class="collapsed ? 'bi-chevron-double-right' : 'bi-chevron-double-left'"></i>
        </button>
      </div>

      <p v-if="!collapsed" class="sidebar-section-title">Aplicaciones</p>
      <nav class="sidebar-nav">
        <RouterLink
          v-for="item in navigation"
          :key="item.route"
          :to="item.route"
          class="nav-link-item"
          active-class="is-active"
          :title="collapsed ? item.label : ''"
        >
          <i class="bi" :class="item.icon"></i>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div v-if="!collapsed" class="sidebar-footer">
        <div class="sidebar-footer-card">
          <div class="sidebar-user-head">
            <div class="sidebar-user-copy">
              <span class="sidebar-user-kicker">Sesion activa</span>
              <strong>{{ currentUser?.full_name || "Sin sesion" }}</strong>
            </div>
            <div class="sidebar-user-status sidebar-user-status-inline" :class="{ online: Boolean(currentUser?.is_active) }">
              <span class="status-dot"></span>
              <span>{{ currentUser?.is_active ? "Activo" : "Inactivo" }}</span>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <div class="app-main">
      <header class="app-topbar">
        <div class="topbar-summary">
          <div>
            <p class="topbar-kicker">Workspace</p>
            <h2 class="topbar-title">{{ currentSection }}</h2>
          </div>
        </div>

        <div class="topbar-actions">
          <Button class="logout-button" severity="secondary" variant="outlined" @click="logout">
            <i class="bi bi-box-arrow-right"></i>
            <span>Salir</span>
          </Button>
        </div>
      </header>

      <div class="app-content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink, RouterView, useRoute, useRouter } from "vue-router";
import Button from "primevue/button";

import { appNavigation as navigation } from "../data/navigation";
import { clearSession, fetchCurrentUser, readStoredUser } from "../services/auth";
import {
  applyBusinessBranding,
  buildAssetUrl,
  fetchPublicBusinessSettings,
  readStoredBusinessSettings,
} from "../services/settings";

const collapsed = ref(false);
const currentUser = ref(readStoredUser());
const businessSettings = ref(
  readStoredBusinessSettings() || {
    business_name: "Orange Tec",
    trade_name: "Orange Tec",
    sidebar_subtitle: "ERP Empresarial",
    logo_sidebar: "",
    logo_favicon: "",
  },
);
const route = useRoute();
const router = useRouter();

const currentSection = computed(() => {
  const current = navigation.find((item) => route.path.startsWith(item.route));
  return current ? current.label : "Panel";
});

const businessLabel = computed(
  () => businessSettings.value?.trade_name || businessSettings.value?.business_name || "Orange Tec",
);

async function hydrateUser() {
  if (!localStorage.getItem("token")) {
    currentUser.value = null;
    return;
  }

  try {
    currentUser.value = await fetchCurrentUser();
    localStorage.setItem("currentUser", JSON.stringify(currentUser.value));
  } catch {
    clearSession();
    currentUser.value = null;
    router.push("/login");
  }
}

async function hydrateBusinessSettings() {
  try {
    businessSettings.value = await fetchPublicBusinessSettings();
    applyBusinessBranding(businessSettings.value);
  } catch {
    // Keep shell usable even if branding config is not available.
  }
}

function logout() {
  clearSession();
  currentUser.value = null;
  router.push("/login");
}

onMounted(() => {
  hydrateBusinessSettings();
  hydrateUser();
  window.addEventListener("business-settings-updated", syncBusinessSettings);
});

function syncBusinessSettings(event) {
  businessSettings.value = event.detail || businessSettings.value;
}

onBeforeUnmount(() => {
  window.removeEventListener("business-settings-updated", syncBusinessSettings);
});
</script>
