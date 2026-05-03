import { createRouter, createWebHistory } from "vue-router";

import { routes } from "./routes";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const isAuthenticated = Boolean(localStorage.getItem("token"));

  if (to.meta.requiresAuth && !isAuthenticated) {
    return "/login";
  }

  if (to.meta.guestOnly && isAuthenticated) {
    return "/app/dashboard";
  }

  return true;
});

export default router;
