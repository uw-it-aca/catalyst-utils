<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-25 ps-0">Created</th>
        <th scope="col">Name</th>
        <th scope="col" class="pe-0" style="width: 110px;">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(gradebook, index) in gradebooks" :key="index">
        <td class="ps-0">
          <div>{{ formatDate(gradebook.created_date) }}</div>
          <div class="small text-muted">{{ gradebook.owner.login_name }}</div>
        </td>
        <td>
          <div>
            <span v-if="gradebook.name == null" class="">null</span>
            <span v-else>{{ gradebook.name }}</span>
          </div>
          <div class="small text-muted">
            Students
              <span v-if="gradebook.participant_count == null" class="badge rounded-pill bg-beige text-dark">0</span>
              <span v-else>{{ gradebook.participant_count }}</span>
          </div>
        </td>
        <td class="pe-0 align-middle text-end">
          <a
            v-show="gradebook.participant_count > 0"
            v-bind:href="gradebook.download_url"
            title="Download gradebook file"
            class="btn btn-dark-beige btn-sm rounded-pill px-3">Download
          </a>
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
  methods: {
    formatDate,
  },
};
</script>
