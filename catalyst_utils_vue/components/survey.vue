<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-25 ps-0">Created</th>
        <th scope="col">Name</th>
        <th scope="col" class="w-25">Info</th>
        <th scope="col" class="pe-0" style="width: 130px;">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(survey, index) in surveys" :key="index">
        <td class="ps-0">
          <div>{{ formatDate(survey.created_date) }}</div>
          <div class="small text-muted">{{ survey.owner.login_name }}</div>
        </td>
        <td>
          <div>
            <span v-if="survey.name == null" class="">null</span>
            <span v-else>{{ survey.name }}</span>
          </div>
          <div class="small text-muted">
            <span v-if="survey.is_research_confidential">Confidential Research Survey</span>
            <span v-else-if="survey.is_research_anonymous">Anonymous Research Survey</span>
          </div>
        </td>
        <td>
          <div class="mt-4 small text-muted d-flex justify-content-between">
            <div>Questions
            <span v-if="survey.question_count == null" class="badge rounded-pill bg-beige text-dark">0</span>
            <span v-else>{{ survey.question_count }}</span>
            </div>
            <div>Responses
            <span v-if="survey.response_count == null" class="badge rounded-pill bg-beige text-dark">0</span>
            <span v-else>{{ survey.response_count }}</span>
            </div>
          </div>
        </td>
        <td class="pe-0 align-middle text-end">
          <button type="button" class="btn btn-dark-beige btn-sm rounded-pill">Download</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { formatDate } from '../helpers/utils';

export default {
  name: 'survey',
  props: {
    surveys: {
      type: Array,
      required: true,
    },
  },
  methods: {
    formatDate,
  },
};
</script>
