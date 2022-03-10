<template>
  <table class="table mb-0">
    <thead>
      <tr>
        <th scope="col">Created</th>
        <th scope="col">Name</th>
        <th scope="col">Info</th>
        <th scope="col" style="width: 130px;">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="index in 4" :key="index">
        <td class="placeholder-glow">
          <div><span class="placeholder col-12"></span></div>
          <div><span class="placeholder col-7"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder col-6"></span></div>
          <div><span class="placeholder col-10"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder col-12"></span></div>
        </td>
        <td>
          <button type="button" disabled class="btn btn-sm placeholder">Download</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
