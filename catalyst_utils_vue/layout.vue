<template>
  <!-- layout.vue: this is where you override the layout -->
  <topbar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #header></template>
    <template #main>
      <!-- main section override -->
      <slot name="title">
        <h1>{{ pageTitle }}</h1>
      </slot>
      <slot name="content"></slot>
    </template>
    <template #footer>
      <div class="bg-dark">
        <div class="container-xl py-3 small">
          <div
            class="text-white font-weight-light"
          >Copyright &copy; {{ new Date().getFullYear() }} University of Washington</div>
        </div>
      </div>
    </template>
  </topbar>
</template>

<script>
import { Topbar } from 'axdd-components';

export default {
  name: 'Catalyst Utilities',
  components: {
    'topbar': Topbar,
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
      appName: 'Catalyst Utilities',
      appRootUrl: '/',
      userName: 'javerage',
      signOutUrl: document.body.getAttribute('data-logout-url'),

      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
};
</script>

<style lang="scss" scoped></style>
