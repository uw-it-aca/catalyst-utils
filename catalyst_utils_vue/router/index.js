import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

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
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/gradebooks",
    component: Gradebooks,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// vue-gtag-next router tracking
trackRouter(router);

export default router;
