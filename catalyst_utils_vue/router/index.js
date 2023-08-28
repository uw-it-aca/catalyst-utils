import { createWebHistory, createRouter } from "vue-router";

// page components
import Surveys from "@/pages/surveys.vue";
import Gradebooks from "@/pages/gradebooks.vue";

const routes = [
  {
    path: "/",
    redirect: "/surveys",
  },
  {
    path: "/surveys",
    component: Surveys,
  },
  {
    path: "/gradebooks",
    component: Gradebooks,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
