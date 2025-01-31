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
import DatasetPage from "@/pages/Dataset.vue";
import ModelPage from "@/pages/Model.vue";
import ModelDetail from "@/pages/ModelDetail.vue";
import DatasetDetail from "@/pages/DatasetDetail.vue";
import TrainingPage from "@/pages/Training.vue";
import TrainingDetail from "@/pages/TrainingDetail.vue";

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
    {
      path: "/dataset",
      name: "dataset",
      component: DatasetPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/dataset/:id",
      name: "dataset_detail",
      component: DatasetDetail,
      meta: { requiresAuth: true },
    },
    {
      path: "/model",
      name: "model",
      component: ModelPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/model/:id",
      name: "model_detail",
      component: ModelDetail,
      meta: { requiresAuth: true },
    },
    {
      path: "/training",
      name: "training",
      component: TrainingPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/training/:id",
      name: "training_detail",
      component: TrainingDetail,
      meta: { requiresAuth: true },
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
