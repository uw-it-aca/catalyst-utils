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
      <tr v-for="index in 3" :key="index">
        <td class="ps-0 placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
          <div><span class="placeholder bg-light-gray col-5"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
          <div><span class="placeholder bg-light-gray col-7"></span></div>
        </td>
        <td class="pe-0 align-middle text-end">
          <button type="button" disabled class="btn btn-sm placeholder bg-light-gray text-muted rounded-pill px-3">Download</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
