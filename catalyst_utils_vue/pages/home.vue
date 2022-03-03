// home.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row">
        <div class="col">

          <div class="mb-3">{{ surveyData }}</div>

          <h2>Your Surveys</h2>

          <p>{{ surveyData.owned_surveys }}</p>
          <p>{{ surveyData.owned_surveys.length }}</p>
          <p>{{ typeof surveyData.owned_surveys }}</p>

          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <table v-if="surveyData.owned_surveys" class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(owned, index) in surveyData.owned_surveys" :key="index">
                    <td>
                      <div>{{ formatDate(owned.created_date) }}</div>
                      <div class="small">{{ owned.owner.login_name }}</div>
                    </td>
                    <td>
                      <span v-if="owned.name == null" class="text-muted"
                        >null</span
                      >
                      <span v-else>{{ owned.name }}</span>
                    </td>
                    <td>
                      <div>
                        Questions:
                        <span v-if="owned.question_count == null" class="text-muted"
                          >null</span
                        >
                        <span v-else>{{ owned.question_count }}</span>

                        Responses:
                        <span v-if="owned.response_count == null" class="text-muted"
                          >null</span
                        >
                        <span v-else>{{ owned.response_count }}</span>
                      </div>
                      <div>
                        Anonymous: {{ owned.is_research_anonymous }} Confidential:
                        {{ owned.is_research_confidential }}
                      </div>
                    </td>
                    <td><button type="button" class="btn btn-dark-beige btn-sm">Download</button></td>
                  </tr>
                </tbody>
              </table>
              <div v-else>No data</div>
            </div>
          </div>

          <h2>Surveys Owned by Others Netids</h2>

          <p>{{ surveyData.netid_surveys }}</p>
          <p>{{ surveyData.netid_surveys.length }}</p>
          <p>{{ typeof surveyData.netid_surveys }}</p>

          <div class="card mb-5">
            <div class="card-body table-responsive-md">

              <table v-if="!surveyData.netid_surveys == '[]'" class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(netid, index) in surveyData.netid_surveys" :key="index">
                    <td>
                      <div>{{ formatDate(netid.created_date) }}</div>
                      <div class="small">{{ netid.owner.login_name }}</div>
                    </td>
                    <td>
                      <span v-if="netid.name == null" class="text-muted"
                        >null</span
                      >
                      <span v-else>{{ netid.name }}</span>
                    </td>
                    <td>
                      <div>
                        Questions:
                        <span v-if="netid.question_count == null" class="text-muted"
                          >null</span
                        >
                        <span v-else>{{ netid.question_count }}</span>

                        Responses:
                        <span v-if="netid.response_count == null" class="text-muted"
                          >null</span
                        >
                        <span v-else>{{ netid.response_count }}</span>
                      </div>
                      <div>
                        Anonymous: {{ netid.is_research_anonymous }} Confidential:
                        {{ netid.is_research_confidential }}
                      </div>
                    </td>
                    <td><button type="button" class="btn btn-darl-beige btn-sm">Download</button></td>
                  </tr>
                </tbody>
              </table>
              <div v-else>No data</div>
            </div>
          </div>

          <h2>Surveys you have Admin access to</h2>

          <p>{{ surveyData.admin_surveys }}</p>
          <p>{{ surveyData.admin_surveys.length }}</p>
          <p>{{ typeof surveyData.admin_surveys }}</p>

          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <table v-if="!surveyData.admin_surveys == '[]'" class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(admin, index) in surveyData.admin_surveys" :key="index">
                    <td>
                      <div>{{ formatDate(admin.created_date) }}</div>
                      <div class="small">{{ admin.owner.login_name }}</div>
                    </td>
                    <td>
                      <span v-if="admin.name == null" class="text-muted"
                        >null</span
                      >
                      <span v-else>{{ admin.name }}</span>
                    </td>
                    <td>
                      <div>
                        Questions:
                        <span v-if="admin.question_count == null" class="text-muted"
                          >null</span
                        >
                        <span v-else>{{ admin.question_count }}</span>

                        Responses:
                        <span v-if="admin.response_count == null" class="text-muted"
                          >null</span
                        >
                        <span v-else>{{ admin.response_count }}</span>
                      </div>
                      <div>
                        Anonymous: {{ admin.is_research_anonymous }} Confidential:
                        {{ admin.is_research_confidential }}
                      </div>
                    </td>
                    <td><button type="button" class="btn btn-dark-beige btn-sm">Download</button></td>
                  </tr>
                </tbody>
              </table>
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
import dayjs from 'dayjs';

export default {
  components: {
    layout: Layout,
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
        });
    },
    formatDate(dateString) {
      const date = dayjs(dateString);
      // Then specify how you want your dates to be formatted
      return date.format('MMMM D, YYYY');
    }
  },
  created() {
    // fetch the survey data
    this.getSurveyData();
  }
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
