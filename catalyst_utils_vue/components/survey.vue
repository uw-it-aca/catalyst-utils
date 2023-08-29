<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-50">Name</th>
        <th scope="col">&nbsp;</th>
        <th scope="col">Created</th>
        <th scope="col">Owner</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr v-for="(survey, index) in surveys" :key="index">
        <td>
          <div>
            <span v-if="survey.name == null" class="">null</span>
            <span v-else>{{ survey.name }}</span>
          </div>
          <div class="small text-muted d-flex">
            <div class="me-4">
              Questions
              <span class="badge rounded-pill bg-beige text-dark">{{
                survey.question_count
              }}</span>
            </div>
            <div class="me-4">
              Responses
              <span class="badge rounded-pill bg-beige text-dark">{{
                survey.response_count
              }}</span>
            </div>
            <div>
              <span v-if="survey.is_research_confidential"
                >Confidential Research Survey</span
              >
              <span v-else-if="survey.is_research_anonymous"
                >Anonymous Research Survey</span
              >
            </div>
          </div>
        </td>
        <td class="align-middle">
          <a
            v-show="survey.question_count > 0 || survey.response_count > 0"
            v-bind:href="survey.download_url"
            title="Download survey files"
            class="btn btn-outline-dark-beige btn-sm rounded-pill px-3"
            >Download
          </a>
        </td>
        <td>
          <div class="small text-muted">
            {{ formatDate(survey.created_date) }}
          </div>
        </td>
        <td>
          <div class="small text-muted">{{ survey.owner.login_name }}</div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { formatDate } from "@/helpers/utils";

export default {
  name: "SurveyComp",
  props: {
    surveys: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      userName: document.body.getAttribute("data-user-name"),
    };
  },
  methods: {
    formatDate,
  },
};
</script>

<style lang="scss">
.table tbody {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
