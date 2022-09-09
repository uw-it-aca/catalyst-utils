<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading>
              <axdd-card-heading :level="2">Gradebooks</axdd-card-heading>
            </template>
            <template #body>
              <axdd-tabs :tabs-id="'gradebooks'">
                <template #items>
                  <axdd-tab-item :tabs-id="'gradebooks'" :panel-id="'owner'" :active-tab="true"
                    >Owner
                    <span
                      v-if="gradebookData.owned_gradebooks && gradebookData.owned_gradebooks.length"
                      class="badge rounded-pill bg-purple text-white"
                      >{{ gradebookData.owned_gradebooks.length }}</span
                    ></axdd-tab-item
                  >
                  <axdd-tab-item :tabs-id="'gradebooks'" :panel-id="'collab'"
                    >Collaborator
                    <span
                      v-if="gradebookData.admin_gradebooks && gradebookData.admin_gradebooks.length"
                      class="badge rounded-pill bg-purple text-white"
                      >{{ gradebookData.admin_gradebooks.length }}</span
                    ></axdd-tab-item
                  >
                  <axdd-tab-item :tabs-id="'gradebooks'" :panel-id="'shared'"
                    >Shared-account Admin
                    <span
                      v-if="gradebookData.netid_gradebooks && gradebookData.netid_gradebooks.length"
                      class="badge rounded-pill bg-purple text-white"
                      >{{ gradebookData.netid_gradebooks.length }}</span
                    ></axdd-tab-item
                  >
                </template>
                <template #panels>
                  <table-loading v-if="isLoading"></table-loading>
                  <axdd-tab-panel v-else :panel-id="'owner'" :active-panel="true">
                    <div
                      v-if="gradebookData.owned_gradebooks && gradebookData.owned_gradebooks.length"
                    >
                      <gradebook :gradebooks="gradebookData.owned_gradebooks" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tab-panel>
                  <axdd-tab-panel :panel-id="'collab'">
                    <div
                      v-if="gradebookData.admin_gradebooks && gradebookData.admin_gradebooks.length"
                    >
                      <gradebook :gradebooks="gradebookData.admin_gradebooks" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tab-panel>
                  <axdd-tab-panel :panel-id="'shared'">
                    <div
                      v-if="gradebookData.netid_gradebooks && gradebookData.netid_gradebooks.length"
                    >
                      <gradebook :gradebooks="gradebookData.netid_gradebooks" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tab-panel>
                </template>
              </axdd-tabs>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import { Card, CardHeading, Tabs, TabItem, TabPanel } from 'axdd-components';
import Layout from '../layout.vue';
import Gradebook from '../components/gradebook.vue';
import TableLoading from '../components/table-loading.vue';

export default {
  components: {
    'layout': Layout,
    'gradebook': Gradebook,
    'table-loading': TableLoading,
    'axdd-card': Card,
    'axdd-card-heading': CardHeading,
    'axdd-tabs': Tabs,
    'axdd-tab-item': TabItem,
    'axdd-tab-panel': TabPanel,
  },
  data() {
    return {
      pageTitle: 'Gradebooks',
      gradebookData: [],
      isLoading: true,
    };
  },
  methods: {
    getGradebookData() {
      fetch('/api/v1/gradebook')
        .then((response) => response.json())
        .then((data) => {
          this.gradebookData = data;
          this.isLoading = false;
        })
        .catch((error) => {
          this.requestError = error;
        });
    },
  },
  mounted() {
    this.getGradebookData();
    //setTimeout(this.getGradebookData, 3000);
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
