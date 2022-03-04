// home.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row">
        <div class="col">
          <div class="mb-3">{{ gradebookData }}</div>

          <h2>Your Gradebooks</h2>
          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <table v-if="gradebookData.owned_gradebooks && gradebookData.owned_gradebooks.length" class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(owned, index) in gradebookData.owned_gradebooks" :key="index">
                    <td>
                      <div>{{ formatDate(owned.created_date) }}</div>
                      <div class="small">{{ owned.owner.login_name }}</div>
                    </td>
                    <td>
                      <span v-if="owned.name == null" class="text-muted">null</span>
                      <span v-else>{{ owned.name }}</span>
                    </td>
                    <td>
                      <div>
                        Questions:
                        <span v-if="owned.question_count == null" class="text-muted">null</span>
                        <span v-else>{{ owned.question_count }}</span>

                        Responses:
                        <span v-if="owned.response_count == null" class="text-muted">null</span>
                        <span v-else>{{ owned.response_count }}</span>
                      </div>
                      <div>
                        Anonymous: {{ owned.is_research_anonymous }} Confidential:
                        {{ owned.is_research_confidential }}
                      </div>
                    </td>
                    <td>
                      <button type="button" class="btn btn-dark-beige btn-sm">Download</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else>No data</div>
            </div>
          </div>

          <h2>Gradebooks Owned by Others Netids</h2>
          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <table v-if="gradebookData.netid_gradebooks && gradebookData.netid_gradebooks.length" class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(netid, index) in gradebookData.netid_gradebooks" :key="index">
                    <td>
                      <div>{{ formatDate(netid.created_date) }}</div>
                      <div class="small">{{ netid.owner.login_name }}</div>
                    </td>
                    <td>
                      <span v-if="netid.name == null" class="text-muted">null</span>
                      <span v-else>{{ netid.name }}</span>
                    </td>
                    <td>
                      <div>
                        Questions:
                        <span v-if="netid.question_count == null" class="text-muted">null</span>
                        <span v-else>{{ netid.question_count }}</span>

                        Responses:
                        <span v-if="netid.response_count == null" class="text-muted">null</span>
                        <span v-else>{{ netid.response_count }}</span>
                      </div>
                      <div>
                        Anonymous: {{ netid.is_research_anonymous }} Confidential:
                        {{ netid.is_research_confidential }}
                      </div>
                    </td>
                    <td>
                      <button type="button" class="btn btn-darl-beige btn-sm">Download</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else>No data</div>
            </div>
          </div>

          <h2>Gradebooks you have Admin access to</h2>
          <div class="card mb-5">
            <div class="card-body table-responsive-md">
              <table v-if="gradebookData.admin_gradebooks && gradebookData.admin_gradebooks.length" class="table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Created</th>
                    <th scope="col">Name</th>
                    <th scope="col">Info</th>
                    <th scope="col">&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(admin, index) in gradebookData.admin_gradebooks" :key="index">
                    <td>
                      <div>{{ formatDate(admin.created_date) }}</div>
                      <div class="small">{{ admin.owner.login_name }}</div>
                    </td>
                    <td>
                      <span v-if="admin.name == null" class="text-muted">null</span>
                      <span v-else>{{ admin.name }}</span>
                    </td>
                    <td>
                      <div>
                        Questions:
                        <span v-if="admin.question_count == null" class="text-muted">null</span>
                        <span v-else>{{ admin.question_count }}</span>

                        Responses:
                        <span v-if="admin.response_count == null" class="text-muted">null</span>
                        <span v-else>{{ admin.response_count }}</span>
                      </div>
                      <div>
                        Anonymous: {{ admin.is_research_anonymous }} Confidential:
                        {{ admin.is_research_confidential }}
                      </div>
                    </td>
                    <td>
                      <button type="button" class="btn btn-dark-beige btn-sm">Download</button>
                    </td>
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
      pageTitle: 'Gradebooks',
      gradebookData: [],
    };
  },
  methods: {
    getGradebookData() {
      fetch('/api/v1/gradebook')
        .then((response) => response.json())
        .then((data) => {
          this.gradebookData = data;
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
    this.getGradebookData();
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
