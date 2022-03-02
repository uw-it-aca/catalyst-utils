<template>
  <!-- layout.vue: this is where you override the layout -->
  <sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header>
    </template>
    <template #navigation>
      <ul class="text-white">
        <li>Surveys</li>
        <li>Gradebooks</li>
      </ul>
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
