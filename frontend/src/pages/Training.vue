<template>
  <fwb-table class="mt-5">
    <fwb-table-head>
      <fwb-table-head-cell>ID</fwb-table-head-cell>
      <fwb-table-head-cell>Experiment Name</fwb-table-head-cell>
      <fwb-table-head-cell>Precision</fwb-table-head-cell>
      <fwb-table-head-cell>Recall</fwb-table-head-cell>
      <fwb-table-head-cell>Model Name</fwb-table-head-cell>
      <fwb-table-head-cell>Dataset Name</fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body v-for="(data, index) in listData" :key="index">
      <fwb-table-row>
        <fwb-table-cell>{{ index + 1 }}</fwb-table-cell>
        <fwb-table-cell>{{ data.experiment_name }}</fwb-table-cell>
        <fwb-table-cell>{{ data.precision }}</fwb-table-cell>
        <fwb-table-cell>{{ data.recall }}</fwb-table-cell>
        <fwb-table-cell>{{ data.model.name }}</fwb-table-cell>
        <fwb-table-cell>{{ data.dataset.name }}</fwb-table-cell>
        <fwb-table-cell>
          <fwb-button @click="goDetail(data.id)" class="btn bg-blue-700">Detail</fwb-button>
        </fwb-table-cell>
      </fwb-table-row>
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import {
  FwbButton,
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
} from "flowbite-vue";
import { useTrainingStore } from "@/store/modules/trainings";
import { useRouter } from "vue-router";

const router = useRouter();
const listData = ref();
const store = useTrainingStore();
const fetchData = () => {
  store.getList().then((res) => {
    listData.value = res;
  });
};

const goDetail = (id: number) => {
  router.push(`/training/${id}`);
};

onMounted(() => {
  fetchData();
});

</script>
