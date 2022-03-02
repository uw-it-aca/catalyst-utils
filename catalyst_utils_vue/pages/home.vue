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
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Owner</th>
                    <th scope="col">Info</th>
                    <th scope="col">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(ownedSurvey, index) in surveyDataList.owned_surveys">
                    <td>{{ ownedSurvey.created_date }}</td>
                    <td>{{ ownedSurvey.name }}</td>
                    <td>{{ ownedSurvey.owner.login_name }}, {{ ownedSurvey.owner.name }}</td>
                    <td>
                      Questions:{{ ownedSurvey.question_count }} Responses:
                      {{ ownedSurvey.response_count }}
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
  },
  mounted() {
    this.getSurveyData();
  },
};
</script>

<style lang="scss"></style>
