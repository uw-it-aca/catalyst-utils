<template>
  <!-- layout.vue: this is where you override the layout -->
  <sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header></template>
    <template #navigation>
      <ul class="nav flex-column mb-5">
        <li class="nav-item mb-1">
          <router-link
            class="nav-link text-light bg-dark-purple-hover rounded me-1 px-2 py-1"
            active-class="bg-dark-purple"
            :to="'/surveys'"
            ><i class="bi bi-check-lg me-2"></i>WebQ Surveys</router-link
          >
        </li>
        <li class="nav-item mb-1">
          <router-link
            class="nav-link text-light bg-dark-purple-hover rounded me-1 px-2 py-1"
            active-class="bg-dark-purple"
            :to="'/gradebooks'"
            ><i class="bi bi-percent me-2"></i>GradeBooks</router-link
          >
        </li>
      </ul>
      <p class="text-light-gray bg-dark-purple rounded-3 p-3 small">
        Welcome to the Catalyst Archive tool!
        <br/><br/>
        Catalyst WebQ and GradeBook will retire on June 16, 2022. This self-service archive enables you to download your WebQ surveys and responses, and GradeBook CSV files.
        <br/><br/>
        <a href="https://itconnect.uw.edu/learn/tools/catalyst-web-tools/retirement/" target="blank">Learn more</a>
      </p>
      <br /><br />
    </template>
    <template #main>
      <!-- main section override -->
      <slot name="title">
        <h1 class="visually-hidden">{{ pageTitle }}</h1>
      </slot>

        <slot name="content"></slot>

    </template>
    <template #footer> </template>
  </sidebar>
</template>

<script>
import { Sidebar } from 'axdd-components';

export default {
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
      userName: document.body.getAttribute('data-user-name'),
      signOutUrl: document.body.getAttribute('data-signout-url'),

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
