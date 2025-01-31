<template>
  <div>
    <label for="fruits">Select Fruits</label>
    <select v-model="datasets" multiple>
      <option  v-for="(data, index) in datasetOptions" :key="index" :value="data.id">{{ data.name }}</option>
    </select>
  </div>
  <fwb-button @click="training" class="btn btn-primary mt-4">Training</fwb-button>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import { FwbButton } from "flowbite-vue";
import { useModelStore } from "@/store/modules/models";
import { useImageStore } from "@/store/modules/images";
import { useTrainingStore } from "@/store/modules/trainings";
import { useRoute } from "vue-router";
import { useNotificationStore } from "@/store/modules/notifications";

const route = useRoute();
const store = useModelStore();
const imageStore = useImageStore();
const trainingStore = useTrainingStore();
const detailData = ref();
const datasets = ref([]);
const datasetOptions = ref();
const notificationStore = useNotificationStore();

const fetchData = async () => {
  const id = route.params.id;
  store.getDetail(id).then((res) => {
    detailData.value = res;
  });
  imageStore.getList().then((res) => {
    datasetOptions.value = res;
  });
};

const training = async () => {
  try {
    trainingStore.store(detailData.value.id, datasets.value).then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") {
        datasets.value = [];
        fetchData();
      }
    });
  } catch (error) {
    console.log(error);
  }
};

onMounted(() => {
  fetchData();
});

</script>
