import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
  type NavigationGuardNext,
} from "vue-router";
import LoginPage from "@/pages/Login.vue";
import { useUserStore } from "@/store/modules/users";
import DashboardPage from "@/pages/Dashboard.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: DashboardPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: LoginPage,
    },
  ],
});

router.beforeEach(
  (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext
  ) => {
    console.log(`Navigating from ${from.fullPath} to ${to.fullPath}`);

    const store = useUserStore();
    if (to.meta?.requiresAuth && !store.isLoggedIn) next({ name: "login" });

    if (to.name == "login" && store.isLoggedIn) next({ name: "dashboard" });

    next();
  }
);

export default router;
