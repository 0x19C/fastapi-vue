import { createRouter, createWebHistory } from "vue-router";
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

router.beforeEach((to: { meta: { requiresAuth: any; }; }) => {
  const store = useUserStore()
  if (to.meta.requiresAuth && !store.isLoggedIn) return '/login'
})

export default router;
