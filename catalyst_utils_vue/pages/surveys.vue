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
              <div v-if="surveyData.owned_surveys && surveyData.owned_surveys.length">
                <survey :surveys="surveyData.owned_surveys" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>

          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">Owned by Others</h2>
            </div>
            <div v-if="isLoading" class="card-body p-4 pb-0 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="surveyData.netid_surveys && surveyData.netid_surveys.length">
                <survey :surveys="surveyData.netid_surveys" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>

          <div class="card border-light-gray shadow-sm rounded-3 mb-4">
            <div class="card-header bg-white border-0 p-4 pb-0">
              <h2 class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige">You have Admin access</h2>
            </div>
            <div v-if="isLoading" class="card-body p-4 d-flex justify-content-center">
              <table-loading></table-loading>
            </div>
            <div v-else class="card-body p-4">
              <div v-if="surveyData.admin_surveys && surveyData.admin_surveys.length">
                <survey :surveys="surveyData.admin_surveys" />
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
