<template>
  <div class="auth-page">
    <div class="auth-hero">
      <div>
        <p class="auth-kicker">Orange Tec ERP</p>
        <h1>Opera tu empresa desde una sola plataforma.</h1>
        <p class="auth-copy">
          Inventario, ventas, usuarios y control administrativo en una interfaz tipo ERP
          moderna, estructurada para crecer por modulos.
        </p>
      </div>

      <div class="auth-hero-grid">
        <div class="auth-hero-tile">
          <span>Inventario</span>
          <strong>Productos, ingresos y egresos</strong>
        </div>
        <div class="auth-hero-tile">
          <span>Ventas</span>
          <strong>POS y facturacion en construccion</strong>
        </div>
        <div class="auth-hero-tile">
          <span>Control</span>
          <strong>Backoffice administrativo</strong>
        </div>
      </div>
    </div>

    <div class="auth-card">
      <div v-if="branding.logo_login" class="auth-logo-wrap">
        <img :src="buildAssetUrl(branding.logo_login)" :alt="businessLabel || 'Logo negocio'" />
      </div>

      <div class="auth-card-header">
        <h2>Iniciar sesion</h2>
        <p>Accede a {{ businessLabel || "tu entorno empresarial" }} con el usuario principal configurado en el sistema.</p>
      </div>

      <form class="auth-form" @submit.prevent="login">
        <label class="field-group">
          <span>Usuario o correo</span>
          <InputText v-model="email" class="form-control" placeholder="administrador" />
        </label>

        <label class="field-group">
          <span>Contrasena</span>
          <Password
            v-model="password"
            class="form-control"
            placeholder="020416"
            :feedback="false"
            toggle-mask
          />
        </label>

        <Button class="auth-submit" :disabled="loading" type="submit" fluid>
          {{ loading ? "Ingresando..." : "Entrar al ERP" }}
        </Button>

        <p v-if="error" class="auth-error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

import { loginUser, storeSession } from "../../services/auth";
import {
  applyBusinessBranding,
  buildAssetUrl,
  fetchPublicBusinessSettings,
  readStoredBusinessSettings,
} from "../../services/settings";

const router = useRouter();
const email = ref("administrador");
const password = ref("020416");
const error = ref(null);
const loading = ref(false);
const branding = ref(
  readStoredBusinessSettings() || {
    business_name: "Orange Tec",
    trade_name: "Orange Tec",
    logo_login: "",
    logo_favicon: "",
  },
);

const businessLabel = computed(() => branding.value?.trade_name || branding.value?.business_name || "Orange Tec");

async function login() {
  error.value = null;
  loading.value = true;

  try {
    const data = await loginUser({
      email: email.value,
      password: password.value,
    });
    storeSession(data);
    router.push("/app/dashboard");
  } catch (err) {
    error.value = err.message || "No se pudo iniciar sesion";
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  try {
    branding.value = await fetchPublicBusinessSettings();
    applyBusinessBranding(branding.value);
  } catch {
    // Ignore branding errors on login screen.
  }
});
</script>
