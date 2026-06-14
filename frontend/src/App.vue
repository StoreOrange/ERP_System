<template>
  <Toast position="top-right" />
  <ConfirmDialog />
  <router-view />
</template>

<script setup>
import ConfirmDialog from "primevue/confirmdialog";
import Toast from "primevue/toast";
</script>
