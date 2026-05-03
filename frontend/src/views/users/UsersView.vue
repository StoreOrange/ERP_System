<template>
  <section class="page-section users-page">
    <header class="module-hero">
      <div class="module-hero-copy">
        <p class="page-kicker">Seguridad</p>
        <h1 class="page-title">Usuarios y accesos</h1>
        <p class="panel-text">
          Punto de entrada para roles, permisos y trazabilidad administrativa del ERP.
        </p>
      </div>
      <div class="module-hero-meta">
        <div class="module-meta-box">
          <span>Perfil visible</span>
          <strong>{{ currentRole }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Acceso</span>
          <strong>{{ currentUser?.is_active ? "Habilitado" : "Restringido" }}</strong>
        </div>
        <div class="module-meta-box">
          <span>Estado</span>
          <strong>Base activa</strong>
        </div>
      </div>
    </header>

    <div class="content-grid single-column">
      <section class="panel-card">
        <div class="panel-head">
          <h3>Estado del modulo</h3>
        </div>
        <p class="panel-text">
          Este espacio queda listo para crecer hacia roles, permisos, sucursales y
          configuracion de usuarios. La ruta ya es visible y consistente con el resto del ERP.
        </p>
      </section>

      <section class="panel-card">
        <div class="panel-head">
          <h3>Sesion actual</h3>
        </div>
        <div class="info-table">
          <div class="info-row">
            <span>Nombre</span>
            <strong>{{ currentUser?.full_name || "Sin sesion" }}</strong>
          </div>
          <div class="info-row">
            <span>Email</span>
            <strong>{{ currentUser?.email || "Sin identificador" }}</strong>
          </div>
          <div class="info-row">
            <span>Rol</span>
            <strong>{{ currentRole }}</strong>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";

import { readStoredUser } from "../../services/auth";

const currentUser = readStoredUser();

const currentRole = computed(() => {
  const roles = currentUser?.roles || [];
  return roles.length ? roles[0].name : "Sin rol";
});
</script>
