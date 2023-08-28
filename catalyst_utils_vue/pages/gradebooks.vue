<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #body>
              <axdd-card-heading :level="2" class="my-2"
                >Gradebooks</axdd-card-heading
              >
              <axdd-tabs-list :tabs-id="'gradebooks'" class="mb-3">
                <template #items>
                  <axdd-tabs-item
                    :tabs-id="'gradebooks'"
                    :panel-id="'owner'"
                    :active-tab="true"
                    >Owner
                    <span
                      v-if="
                        gradebookData.owned_gradebooks &&
                        gradebookData.owned_gradebooks.length
                      "
                      class="badge rounded-pill bg-purple text-white"
                      >{{ gradebookData.owned_gradebooks.length }}</span
                    ></axdd-tabs-item
                  >
                  <axdd-tabs-item :tabs-id="'gradebooks'" :panel-id="'collab'"
                    >Collaborator
                    <span
                      v-if="
                        gradebookData.admin_gradebooks &&
                        gradebookData.admin_gradebooks.length
                      "
                      class="badge rounded-pill bg-purple text-white"
                      >{{ gradebookData.admin_gradebooks.length }}</span
                    ></axdd-tabs-item
                  >
                  <axdd-tabs-item :tabs-id="'gradebooks'" :panel-id="'shared'"
                    >Shared-account Admin
                    <span
                      v-if="
                        gradebookData.netid_gradebooks &&
                        gradebookData.netid_gradebooks.length
                      "
                      class="badge rounded-pill bg-purple text-white"
                      >{{ gradebookData.netid_gradebooks.length }}</span
                    ></axdd-tabs-item
                  >
                </template>
              </axdd-tabs-list>

              <axdd-tabs-display :tabs-id="'gradebooks'">
                <template #panels>
                  <table-loading v-if="isLoading"></table-loading>
                  <axdd-tabs-panel
                    v-else
                    :panel-id="'owner'"
                    :active-panel="true"
                  >
                    <div
                      v-if="
                        gradebookData.owned_gradebooks &&
                        gradebookData.owned_gradebooks.length
                      "
                    >
                      <gradebook :gradebooks="gradebookData.owned_gradebooks" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tabs-panel>
                  <axdd-tabs-panel :panel-id="'collab'">
                    <div
                      v-if="
                        gradebookData.admin_gradebooks &&
                        gradebookData.admin_gradebooks.length
                      "
                    >
                      <gradebook :gradebooks="gradebookData.admin_gradebooks" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tabs-panel>
                  <axdd-tabs-panel :panel-id="'shared'">
                    <div
                      v-if="
                        gradebookData.netid_gradebooks &&
                        gradebookData.netid_gradebooks.length
                      "
                    >
                      <gradebook :gradebooks="gradebookData.netid_gradebooks" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tabs-panel>
                </template>
              </axdd-tabs-display>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import {
  Card,
  CardHeading,
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";
import Layout from "@/layout.vue";
import Gradebook from "@/components/gradebook.vue";
import TableLoading from "@/components/table-loading.vue";

export default {
  name: "PagesGradebooksComp",
  components: {
    layout: Layout,
    gradebook: Gradebook,
    "table-loading": TableLoading,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
  },
  data() {
    return {
      pageTitle: "Gradebooks",
      gradebookData: [],
      isLoading: true,
    };
  },
  methods: {
    getGradebookData() {
      fetch("/api/v1/gradebook")
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
