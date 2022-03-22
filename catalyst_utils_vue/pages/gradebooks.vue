<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">Yours</h2>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="gradebookData.owned_gradebooks && gradebookData.owned_gradebooks.length">
                <gradebook :gradebooks="gradebookData.owned_gradebooks" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>

          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">Owned by Others</h2>
            </div>
            <div v-if="isLoading" class="card-body p-4 pt-0 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="gradebookData.netid_gradebooks && gradebookData.netid_gradebooks.length">
                <gradebook :gradebooks="gradebookData.netid_gradebooks" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>

          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">You have Admin access</h2>
            </div>
            <div v-if="isLoading" class="card-body p-4 pt-0 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="gradebookData.admin_gradebooks && gradebookData.admin_gradebooks.length">
                <gradebook :gradebooks="gradebookData.admin_gradebooks" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import Gradebook from '../components/gradebook.vue';
import TableLoading from '../components/table-loading.vue';

export default {
  components: {
    'layout': Layout,
    'gradebook': Gradebook,
    'table-loading': TableLoading
  },
  data() {
    return {
      pageTitle: 'Gradebooks',
      gradebookData: [],
      isLoading: true,
    };
  },
  methods: {
    getGradebookData() {
      fetch('/api/v1/gradebook')
        .then((response) => response.json())
        .then((data) => {
          this.gradebookData = data;
          this.isLoading = false;
        })
        .catch((error) => {
          // Do something useful with the error
        });
    },
  },
  mounted() {
    this.getGradebookData();
    //setTimeout(this.getGradebookData, 3000);
  },
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
