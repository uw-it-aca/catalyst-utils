<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #body>
              <axdd-card-heading :level="2" class="my-2"
                >WebQ Surveys</axdd-card-heading
              >
              <axdd-tabs-list :tabs-id="'surveys'" class="mb-3">
                <template #items>
                  <axdd-tabs-item
                    :tabs-id="'surveys'"
                    :panel-id="'owner'"
                    :active-tab="true"
                    >Owner
                    <span
                      v-if="
                        surveyData.owned_surveys &&
                        surveyData.owned_surveys.length
                      "
                      class="badge rounded-pill bg-purple text-white"
                      >{{ surveyData.owned_surveys.length }}</span
                    ></axdd-tabs-item
                  >
                  <axdd-tabs-item :tabs-id="'surveys'" :panel-id="'collab'"
                    >Collaborator
                    <span
                      v-if="
                        surveyData.admin_surveys &&
                        surveyData.admin_surveys.length
                      "
                      class="badge rounded-pill bg-purple text-white"
                      >{{ surveyData.admin_surveys.length }}</span
                    ></axdd-tabs-item
                  >
                  <axdd-tabs-item :tabs-id="'surveys'" :panel-id="'shared'"
                    >Shared-account Admin
                    <span
                      v-if="
                        surveyData.netid_surveys &&
                        surveyData.netid_surveys.length
                      "
                      class="badge rounded-pill bg-purple text-white"
                      >{{ surveyData.netid_surveys.length }}</span
                    ></axdd-tabs-item
                  >
                </template>
              </axdd-tabs-list>

              <axdd-tabs-display :tabs-id="'surveys'">
                <template #panels>
                  <table-loading v-if="isLoading"></table-loading>
                  <axdd-tabs-panel
                    v-else
                    :panel-id="'owner'"
                    :active-panel="true"
                  >
                    <div
                      v-if="
                        surveyData.owned_surveys &&
                        surveyData.owned_surveys.length
                      "
                    >
                      <survey :surveys="surveyData.owned_surveys" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tabs-panel>
                  <axdd-tabs-panel :panel-id="'collab'">
                    <div
                      v-if="
                        surveyData.admin_surveys &&
                        surveyData.admin_surveys.length
                      "
                    >
                      <survey :surveys="surveyData.admin_surveys" />
                    </div>
                    <div v-else>No data</div>
                  </axdd-tabs-panel>
                  <axdd-tabs-panel :panel-id="'shared'">
                    <div
                      v-if="
                        surveyData.netid_surveys &&
                        surveyData.netid_surveys.length
                      "
                    >
                      <survey :surveys="surveyData.netid_surveys" />
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
import Layout from "../layout.vue";
import Survey from "../components/survey.vue";
import TableLoading from "../components/table-loading.vue";

export default {
  components: {
    layout: Layout,
    survey: Survey,
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
      pageTitle: "Surveys",
      surveyData: [],
      isLoading: true,
    };
  },
  methods: {
    getSurveyData() {
      fetch("/api/v1/survey")
        .then((response) => response.json())
        .then((data) => {
          this.surveyData = data;
          this.isLoading = false;
        })
        .catch((error) => {
          this.requestError = error;
        });
    },
  },
  mounted() {
    // fetch the survey data
    this.getSurveyData();
    //setTimeout(this.getSurveyData, 3000);
  },
};
</script>
