<template>
  <table class="table mb-0">
    <thead>
      <tr>
        <th scope="col" class="ps-0">Created</th>
        <th scope="col">Name</th>
        <th scope="col">Info</th>
        <th scope="col" class="pe-0" style="width: 130px;">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="index in 4" :key="index">
        <td class="ps-0 placeholder-glow">
          <div><span class="placeholder bg-secondary col-12"></span></div>
          <div><span class="placeholder bg-secondary col-7"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-secondary col-6"></span></div>
          <div><span class="placeholder bg-secondary col-10"></span></div>
        </td>
        <td class="placeholder-glow">
          <div class="mt-4"><span class="placeholder bg-secondary col-12"></span></div>
        </td>
        <td class="pe-0 align-middle text-end">
          <button type="button" disabled class="btn btn-sm placeholder bg-secondary rounded-pill">Download</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
