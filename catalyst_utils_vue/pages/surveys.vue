// home.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row">
        <div class="col">
          <div class="mb-3">{{ surveyData }}</div>

          <h2>Your Surveys</h2>
          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <div v-if="surveyData.owned_surveys && surveyData.owned_surveys.length">
                <survey :surveys="surveyData.owned_surveys" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>

          <h2>Surveys Owned by Shared Netids</h2>
          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <div v-if="surveyData.netid_surveys && surveyData.netid_surveys.length">
                <survey :surveys="surveyData.netid_surveys" />
              </div>
              <div v-else>No data</div>
            </div>
          </div>

          <h2>Surveys you have Admin access to</h2>
          <div class="card mb-5">
            <div class="card-body table-responsive-md">
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
import survey from '@/components/survey.vue'
import dayjs from 'dayjs';

export default {
  components: {
    layout: Layout,
    survey: survey,
  },
  data() {
    return {
      pageTitle: 'Surveys',
      surveyData: [],
    };
  },
  methods: {
    getSurveyData() {
      fetch('/api/v1/survey')
        .then((response) => response.json())
        .then((data) => {
          this.surveyData = data;
        })
        .catch((error) => {
          // Do something useful with the error
        });
    },
    formatDate(dateString) {
      const date = dayjs(dateString);
      // Then specify how you want your dates to be formatted
      return date.format('MMMM D, YYYY');
    },
  },
  mounted() {
    // fetch the survey data
    this.getSurveyData();
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
