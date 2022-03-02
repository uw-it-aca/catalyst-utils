// home.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row">
        <div class="col">
          <h2>Your Surveys</h2>

          <p>
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quos inventore doloremque
            perspiciatis eius enim dicta ad quae? Blanditiis, quaerat voluptas, assumenda
            necessitatibus, quisquam illum eos omnis inventore tempora corporis esse?
          </p>
          <p>
            Lorem ipsum dolor sit, amet consectetur adipisicing elit. Ratione deserunt sapiente,
            ipsam minima praesentium, eaque non animi nemo accusantium quia minus officiis dolorum
            dolores. Quis possimus odit incidunt quaerat officia?
          </p>

          <div class="card mb-5">
            <div class="card-body">
              <table class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Owner</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(ownedSurvey, index) in surveyDataList.owned_surveys">
                    <td>{{ formatDate(ownedSurvey.created_date) }}</td>
                    <td>
                      <span v-if="ownedSurvey.name == null" class="text-muted">survey name null</span>
                      <span v-else>{{ ownedSurvey.name }}</span>
                    </td>
                    <td>{{ ownedSurvey.owner.name }} ({{ ownedSurvey.owner.login_name }})</td>
                    <td>
                      Questions: <span v-if="ownedSurvey.question_count == null">0</span>
                      <span v-else>{{ ownedSurvey.question_count }}</span>

                      Responses: <span v-if="ownedSurvey.response_count == null">0</span>
                      <span v-else>{{ ownedSurvey.response_count }}</span>
                    </td>
                    <td><button type="button" class="btn btn-primary btn-sm">Download</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <h2>Surveys Owned by Others Netids</h2>
          <ul class="list-group mb-5">
            <li class="list-group-item">
              An item
              <button type="button" class="btn btn-primary btn-sm">Download</button>
            </li>
            <li class="list-group-item">
              A second item
              <button type="button" class="btn btn-primary btn-sm">Download</button>
            </li>
            <li class="list-group-item">A third item</li>
            <li class="list-group-item">A fourth item</li>
            <li class="list-group-item">
              And a fifth one | Questions, Responses, Code Translation, Rollup
            </li>
          </ul>

          <h2>Surveys owned by shared netids you have Admin access to</h2>
          <ul class="list-group mb-5">
            <li class="list-group-item">
              An item
              <button type="button" class="btn btn-primary btn-sm">Download</button>
            </li>
            <li class="list-group-item">
              A second item
              <button type="button" class="btn btn-primary btn-sm">Download</button>
            </li>
            <li class="list-group-item">A third item</li>
            <li class="list-group-item">A fourth item</li>
            <li class="list-group-item">
              And a fifth one | Questions, Responses, Code Translation, Rollup
            </li>
          </ul>

          <div class="my-5">{{ surveyDataList }}</div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import dayjs from "dayjs";

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'Surveys',
      surveyDataList: [],
    };
  },
  methods: {
    getSurveyData() {
      fetch('/api/v1/survey')
        .then((response) => response.json())
        .then((data) => (this.surveyDataList = data));
    },
    formatDate(dateString) {
      const date = dayjs(dateString);
      // Then specify how you want your dates to be formatted
      return date.format("MMMM D, YYYY");
    },
  },
  mounted() {
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
