<template>
  <!-- layout.vue: this is where you override the layout -->
  <sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header> </template>
    <template #navigation>
      <ul class="nav flex-column mb-5">
        <li class="nav-item mb-1 bg-dark-purple rounded">
          <a href="#" class="nav-link text-gray d-block px-2 py-1"
            ><i class="bi bi-check-lg me-2"></i>Surveys</a
          >
        </li>
        <li class="nav-item mb-1 bg-dark-purple-hover rounded">
          <a href="#" class="nav-link text-gray d-block px-2 py-1"
            ><i class="bi bi-percent me-2"></i>Gradebooks</a
          >
        </li>
      </ul>
      <p class="text-dark bg-beige rounded p-3 small">
        Welcome... Lorem ipsum dolor, sit amet consectetur adipisicing elit. Cum voluptatibus,
        laborum inventore magni, dolore quod incidunt error reiciendis nesciunt ex atque, amet culpa
        quia ullam sit. Deleniti id at odit!
      </p>
      <br /><br />
    </template>
    <template #main>
      <!-- main section override -->
      <slot name="title">
        <h1>{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer> </template>
  </sidebar>
</template>

<script>
import { Sidebar } from 'axdd-components';

export default {
  name: 'Catalyst',
  components: {
    sidebar: Sidebar,
  },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: 'Catalyst',
      appRootUrl: '/',
      userName: 'javerage',
      signOutUrl: document.body.getAttribute('data-logout-url'),

      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + ' - ' + this.appName;
  },
};
</script>

<style lang="scss" scoped></style>
