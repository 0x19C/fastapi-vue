<template>
  <fwb-img
    alt="Dataset Image"
    :src="imagePath"
  />
  <fwb-range class="mt-5" label="Brightness" v-model="brightness" :max="200" />
  <pre class="mb-5">Current brightness value: {{ brightness }}</pre>
  <fwb-range label="Noise" v-model="noise" />
  <pre>Current noise value: {{ noise }}</pre>
  <fwb-button @click="save" class="btn btn-primary mt-4">Save</fwb-button>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import { FwbImg, FwbRange, FwbButton } from "flowbite-vue";
import { useImageStore } from "@/store/modules/images";
import { useRoute } from "vue-router";
import { useNotificationStore } from "@/store/modules/notifications";

const route = useRoute();
const store = useImageStore();
const detailData = ref();
const brightness = ref(0);
const noise = ref(0);
const imagePath = ref();
const notificationStore = useNotificationStore();

const fetchData = async () => {
  const id = Number(route.params.id);
  store.getDetail(id).then((res) => {
    detailData.value = res;
    imagePath.value = `${import.meta.env.VITE_API_ENDPOINT}/${detailData.value.directory_path}/thumbnail.png`
  });
};

const save = async () => {
  try {
    store.addOper(detailData.value.id, brightness.value, noise.value).then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") {
        brightness.value = 0;
        noise.value = 0;
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
