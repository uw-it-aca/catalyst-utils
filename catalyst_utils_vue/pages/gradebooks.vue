<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">Yours</h2>

              <!-- TODO: componentize -->
              <ul class="nav nav-tabs border-0 mt-3" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                  <button class="nav-link active" id="yours-tab" data-bs-toggle="tab" data-bs-target="#yours" type="button" role="tab" aria-controls="yours" aria-selected="true">Yours</button>
                </li>
                <li class="nav-item" role="presentation">
                  <button class="nav-link" id="others-tab" data-bs-toggle="tab" data-bs-target="#others" type="button" role="tab" aria-controls="others" aria-selected="false">Owned by Others</button>
                </li>
                <li class="nav-item" role="presentation">
                  <button class="nav-link" id="admin-tab" data-bs-toggle="tab" data-bs-target="#admin" type="button" role="tab" aria-controls="admin" aria-selected="false">You have Admin Access</button>
                </li>
              </ul>

            </div>
            <div class="card-body p-4">

              <div v-if="isLoading">
                <table-loading></table-loading>
              </div>

               <!-- TODO: componentize -->
              <div v-else class="tab-content" id="myTabContent">
                <div class="tab-pane fade show active" id="yours" role="tabpanel" aria-labelledby="yours-tab">
                  <div v-if="gradebookData.owned_gradebooks && gradebookData.owned_gradebooks.length">
                    <gradebook :gradebooks="gradebookData.owned_gradebooks" :role="'owner'" />
                  </div>
                  <div v-else>No data</div>
                </div>
                <div class="tab-pane fade" id="others" role="tabpanel" aria-labelledby="others-tab">
                  <div v-if="gradebookData.netid_gradebooks && gradebookData.netid_gradebooks.length">
                    <gradebook :gradebooks="gradebookData.netid_gradebooks" :role="'collaborator'" />
                  </div>
                  <div v-else>No data</div>
                </div>
                <div class="tab-pane fade" id="admin" role="tabpanel" aria-labelledby="admin-tab">
                  <div v-if="gradebookData.admin_gradebooks && gradebookData.admin_gradebooks.length">
                    <gradebook :gradebooks="gradebookData.admin_gradebooks" :role="'collaborator'" />
                  </div>
                  <div v-else>No data</div>
                </div>
              </div>
              <!-- end of tab content -->

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
