import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";
import Surveys from "@/pages/surveys.vue";

const routes = [
  {
    path: "/",
    component: Surveys,
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
