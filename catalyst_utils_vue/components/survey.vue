<template>
  <table class="table mb-0">
    <thead>
      <tr>
        <th scope="col">Created</th>
        <th scope="col">Name</th>
        <th scope="col">Info</th>
        <th scope="col">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(survey, index) in surveys" :key="index">
        <td>
          <div>{{ formatDate(survey.created_date) }}</div>
          <div class="small">{{ survey.owner.login_name }}</div>
        </td>
        <td>
          <span v-if="survey.name == null" class="text-muted">null</span>
          <span v-else>{{ survey.name }}</span>
          <div v-if="survey.is_research_confidential">Confidential Research Survey</div>
          <div v-else-if="survey.is_research_anonymous">Anonymous Research Survey</div>
        </td>
        <td>
          <div>
            Questions:
            <span v-if="survey.question_count == null" class="text-muted">null</span>
            <span v-else>{{ survey.question_count }}</span>

            Responses:
            <span v-if="survey.response_count == null" class="text-muted">null</span>
            <span v-else>{{ survey.response_count }}</span>
          </div>
        </td>
        <td>
          <button type="button" class="btn btn-dark-beige btn-sm">Download</button>
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
        required: true
      }
    },
    methods: {
      formatDate
    }
  };
</script>
