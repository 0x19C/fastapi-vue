import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
  type NavigationGuardNext,
} from "vue-router";
import { useUserStore } from "@/store/modules/users";
import LoginPage from "@/pages/Login.vue";
import DashboardPage from "@/pages/Dashboard.vue";
import RegisterPage from "@/pages/Register.vue";
import NotFoundPage from "@/pages/NotFound.vue";

const router = createRouter({
  history: createWebHistory(),
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
    {
      path: "/register",
      name: "register",
      component: RegisterPage,
    },
    // Wildcard route to handle undefined routes (404)
    {
      path: "/:catchAll(.*)", // This matches any route that is not defined above
      name: "NotFound",
      component: NotFoundPage, // Show the NotFound component for undefined routes
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
