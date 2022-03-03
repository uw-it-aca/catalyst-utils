import { createWebHistory, createRouter } from "vue-router";

// page components
import Surveys from '../pages/surveys.vue';

const routes = [
  {
    path: '/',
    redirect: '/survey'
  },
  {
    path: "/survey",
    component: Surveys
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
