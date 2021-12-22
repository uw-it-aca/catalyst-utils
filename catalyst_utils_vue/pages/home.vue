// home.vue

<template>
  <layout :page-title="pageTitle">
    
    <!--<slot name="title">
        <h1 class="text-danger">{{ pageTitle }}</h1>
      </slot>-->

    <!-- page content -->
    <template #content>
      <div class="row">
        <div class="col">
          <h2>Your Surveys</h2>
          <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quos inventore doloremque perspiciatis eius enim dicta ad quae? Blanditiis, quaerat voluptas, assumenda necessitatibus, quisquam illum eos omnis inventore tempora corporis esse?</p>
          <ul class="list-group mb-5">
            <li class="list-group-item">An item</li>
            <li class="list-group-item">A second item</li>
            <li class="list-group-item">A third item</li>
            <li class="list-group-item">A fourth item</li>
            <li class="list-group-item">And a fifth one</li>
          </ul>

          <h2>Surveys Owned by Others</h2>
           <ul class="list-group">
            <li class="list-group-item">An item</li>
            <li class="list-group-item">A second item</li>
            <li class="list-group-item">A third item</li>
            <li class="list-group-item">A fourth item</li>
            <li class="list-group-item">And a fifth one</li>
          </ul>
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
      pageTitle: 'Downloads',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
