<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-50 ps-0">Name</th>
        <th scope="col">&nbsp;</th>
        <th scope="col">Created</th>
        <th scope="col">Owner</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(gradebook, index) in gradebooks" :key="index">
        <td class="ps-0">
          <div>
            <span v-if="gradebook.name == null" class="">null</span>
            <span v-else>{{ gradebook.name }}</span>
          </div>
          <div class="small text-muted">
            Students
            <span
              v-if="gradebook.participant_count == null"
              class="badge rounded-pill bg-beige text-dark"
              >0</span
            >
            <span v-else class="badge rounded-pill bg-beige text-dark">{{
              gradebook.participant_count
            }}</span>
          </div>
        </td>
        <td class="align-middle">
            <a
              v-show="gradebook.participant_count > 0"
              v-bind:href="gradebook.download_url"
              title="Download gradebook file"
              class="btn btn-outline-dark-beige btn-sm rounded-pill px-3"
              >Download
            </a>
        </td>
        <td>
          <div class="small text-muted">{{ formatDate(gradebook.created_date) }}</div>
        </td>
        <td>
          <div class="small text-muted">{{ gradebook.owner.login_name }}</div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { formatDate } from '../helpers/utils';

export default {
  name: 'gradebook',
  props: {
    gradebooks: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      userName: document.body.getAttribute('data-user-name'),
    };
  },
  methods: {
    formatDate,
  },
};
</script>
