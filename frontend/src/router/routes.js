import AppShell from "../layouts/AppShell.vue";
import DashboardView from "../views/dashboard/DashboardView.vue";
import LoginView from "../views/auth/LoginView.vue";
import ProductsView from "../views/inventory/ProductsView.vue";
import MovementsView from "../views/inventory/MovementsView.vue";
import PacaOpeningView from "../views/inventory/PacaOpeningView.vue";
import ProductionView from "../views/inventory/ProductionView.vue";
import SalesView from "../views/sales/SalesView.vue";
import BusinessSettingsView from "../views/settings/BusinessSettingsView.vue";
import UsersView from "../views/users/UsersView.vue";

export const routes = [
  {
    path: "/",
    redirect: "/app/dashboard",
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: "/app",
    component: AppShell,
    meta: { requiresAuth: true },
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: DashboardView,
      },
      {
        path: "users",
        name: "users",
        component: UsersView,
      },
      {
        path: "products",
        name: "products",
        component: ProductsView,
      },
      {
        path: "inventory/movements",
        name: "inventory-movements",
        component: MovementsView,
      },
      {
        path: "inventory/production",
        name: "inventory-production",
        component: ProductionView,
      },
      {
        path: "inventory/paca-opening",
        name: "inventory-paca-opening",
        component: PacaOpeningView,
      },
      {
        path: "sales",
        name: "sales",
        component: SalesView,
      },
      {
        path: "settings/business",
        name: "business-settings",
        component: BusinessSettingsView,
      },
    ],
  },
  {
    path: "/home",
    redirect: "/app/dashboard",
  },
];
