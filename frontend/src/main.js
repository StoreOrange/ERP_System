import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import PrimeVue from "primevue/config";
import ConfirmationService from "primevue/confirmationservice";
import ToastService from "primevue/toastservice";
import ErpTheme from "./theme/erpTheme";
import { applyBusinessBranding, readStoredBusinessSettings } from "./services/settings";



// Bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import "bootstrap-icons/font/bootstrap-icons.css"
import "./style.css";

applyBusinessBranding(readStoredBusinessSettings());

createApp(App)
  .use(router)
  .use(ToastService)
  .use(ConfirmationService)
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
