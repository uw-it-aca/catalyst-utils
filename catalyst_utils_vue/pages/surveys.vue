<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white p-4 pb-0">
              <h2
                class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
              >
                WebQ Surveys
              </h2>

              <!-- TODO: componentize -->
              <ul class="nav nav-tabs border-0 mt-3" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link active"
                    id="owner-tab"
                    data-bs-toggle="tab"
                    data-bs-target="#owner"
                    type="button"
                    role="tab"
                    aria-controls="owner"
                    aria-selected="true"
                  >
                    Owner
                    <span
                      v-if="surveyData.owned_surveys && surveyData.owned_surveys.length"
                      class="badge rounded-pill bg-beige text-dark"
                      >{{ surveyData.owned_surveys.length }}</span
                    >
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link"
                    id="collaborator-tab"
                    data-bs-toggle="tab"
                    data-bs-target="#collaborator"
                    type="button"
                    role="tab"
                    aria-controls="collaborator"
                    aria-selected="false"
                  >
                    Collaborator
                    <span
                      v-if="surveyData.admin_surveys && surveyData.admin_surveys.length"
                      class="badge rounded-pill bg-beige text-dark"
                      >{{ surveyData.admin_surveys.length }}</span
                    >
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link"
                    id="admin-tab"
                    data-bs-toggle="tab"
                    data-bs-target="#admin"
                    type="button"
                    role="tab"
                    aria-controls="admin"
                    aria-selected="false"
                  >
                    Shared-account Admin
                    <span
                      v-if="surveyData.netid_surveys && surveyData.netid_surveys.length"
                      class="badge rounded-pill bg-beige text-dark"
                      >{{ surveyData.netid_surveys.length }}</span
                    >
                  </button>
                </li>
              </ul>
            </div>
            <div class="card-body p-4">
              <div v-if="isLoading">
                <table-loading></table-loading>
              </div>

              <!-- TODO: componentize -->
              <div v-else class="tab-content" id="myTabContent">
                <div
                  class="tab-pane fade show active"
                  id="owner"
                  role="tabpanel"
                  aria-labelledby="owner-tab"
                >
                  <div v-if="surveyData.owned_surveys && surveyData.owned_surveys.length">
                    <survey :surveys="surveyData.owned_surveys" />
                  </div>
                  <div v-else>No data</div>
                </div>
                <div
                  class="tab-pane fade"
                  id="collaborator"
                  role="tabpanel"
                  aria-labelledby="collaborator-tab"
                >
                  <div v-if="surveyData.admin_surveys && surveyData.admin_surveys.length">
                    <survey :surveys="surveyData.admin_surveys" />
                  </div>
                  <div v-else>No data</div>
                </div>
                <div class="tab-pane fade" id="admin" role="tabpanel" aria-labelledby="admin-tab">
                  <div v-if="surveyData.netid_surveys && surveyData.netid_surveys.length">
                    <survey :surveys="surveyData.netid_surveys" />
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
import Survey from '../components/survey.vue';
import TableLoading from '../components/table-loading.vue';

export default {
  components: {
    layout: Layout,
    survey: Survey,
    'table-loading': TableLoading,
  },
  data() {
    return {
      pageTitle: 'Surveys',
      surveyData: [],
      isLoading: true,
    };
  },
  methods: {
    getSurveyData() {
      fetch('/api/v1/survey')
        .then((response) => response.json())
        .then((data) => {
          this.surveyData = data;
          this.isLoading = false;
        })
        .catch((error) => {
          // Do something useful with the error
        });
    },
  },
  mounted() {
    // fetch the survey data
    this.getSurveyData();
    //setTimeout(this.getSurveyData, 3000);
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
