<template>
  <fwb-heading tag="h3">Training ID</fwb-heading>
  <fwb-p>
    {{ detailData?.id }}
  </fwb-p>
  <fwb-heading tag="h3">Experiment Name</fwb-heading>
  <fwb-p>
    {{ detailData?.experiment_name }}
  </fwb-p>
  <fwb-heading tag="h3">Precision</fwb-heading>
  <fwb-p>
    {{ detailData?.precision }}
  </fwb-p>
  <fwb-heading tag="h3">Recall</fwb-heading>
  <fwb-p>
    {{ detailData?.recall }}
  </fwb-p>
  <fwb-heading tag="h3">Model Name</fwb-heading>
  <fwb-p>
    {{ detailData?.model?.name }}
  </fwb-p>
  <fwb-heading tag="h3">Dataset Name</fwb-heading>
  <fwb-p>
    {{ detailData?.dataset.name }}
  </fwb-p>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import { useTrainingStore } from "@/store/modules/trainings";
import { FwbHeading, FwbP } from "flowbite-vue";
import { useRoute } from "vue-router";

const route = useRoute();
const detailData = ref();
const store = useTrainingStore();

const fetchData = () => {
  const id = route.params.id;
  store.getDetail(id).then((res) => {
    detailData.value = res;
  });
};

onMounted(() => {
  fetchData();
});
</script>