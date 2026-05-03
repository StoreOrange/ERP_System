import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import PrimeVue from "primevue/config";
import "./style.css";
import ErpTheme from "./theme/erpTheme";
import { applyBusinessBranding, readStoredBusinessSettings } from "./services/settings";



// Bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import "bootstrap-icons/font/bootstrap-icons.css"

// HTMX
import htmx from "htmx.org";
window.htmx = htmx;

applyBusinessBranding(readStoredBusinessSettings());

createApp(App)
  .use(router)
  .use(PrimeVue, {
    ripple: true,
    inputVariant: "filled",
    theme: {
      preset: ErpTheme,
      options: {
        darkModeSelector: false,
      },
    },
  })
  .mount("#app");
