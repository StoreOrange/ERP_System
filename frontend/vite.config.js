import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/apexcharts") || id.includes("node_modules/vue3-apexcharts")) {
            return "charts";
          }
          if (id.includes("node_modules/primevue") || id.includes("node_modules/@primeuix")) {
            return "primevue";
          }
          if (id.includes("node_modules/vue") || id.includes("node_modules/vue-router")) {
            return "vue";
          }
          return undefined;
        },
      },
    },
  },
})
