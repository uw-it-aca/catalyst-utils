<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">

          <div class="card border-light-gray shadow-sm rounded-3 mb-4">

            <div class="card-header bg-white p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">Surveys</h2>

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
                  <div v-if="surveyData.owned_surveys && surveyData.owned_surveys.length">
                    <survey :surveys="surveyData.owned_surveys" :role="'owner'" />
                  </div>
                  <div v-else>No data</div>
                </div>
                <div class="tab-pane fade" id="others" role="tabpanel" aria-labelledby="others-tab">
                  <div v-if="surveyData.netid_surveys && surveyData.netid_surveys.length">
                    <survey :surveys="surveyData.netid_surveys" :role="'collaborator'" />
                  </div>
                  <div v-else>No data</div>
                </div>
                <div class="tab-pane fade" id="admin" role="tabpanel" aria-labelledby="admin-tab">
                  <div v-if="surveyData.admin_surveys && surveyData.admin_surveys.length">
                    <survey :surveys="surveyData.admin_surveys" :role="'collaborator'" />
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
    'layout': Layout,
    'survey': Survey,
    'table-loading': TableLoading
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
