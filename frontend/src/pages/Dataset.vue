<template>
  <div class="px-6">
    <fwb-file-input 
      v-model="files" 
      label="Choose files"
      multiple 
      accept="image/*, .zip"
    />
    <fwb-button @click="saveFiles" class="btn btn-primary mt-4">Save</fwb-button>

    <div v-if="files.length !== 0" class="mt-4 border-[1px] border-gray-300 dark:border-gray-600 p-2 rounded-md">
      <div v-for="file in files" :key="file">
        {{ file.name }}
      </div>
    </div>
  </div>

  <div v-if="loading">Uploading...</div>

  <fwb-table class="mt-5">
    <fwb-table-head>
      <fwb-table-head-cell>Dataset</fwb-table-head-cell>
      <fwb-table-head-cell>Color</fwb-table-head-cell>
      <fwb-table-head-cell>Category</fwb-table-head-cell>
      <fwb-table-head-cell>Price</fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body>
      <fwb-table-row>
        <fwb-table-cell>
          <fwb-img
            alt="flowbite-vue"
            img-class="rounded-lg transition-all duration-300 cursor-pointer filter grayscale hover:grayscale-0"
            size="max-w-lg"
            src="./login.png"
          />
        </fwb-table-cell>
        <fwb-table-cell>Sliver</fwb-table-cell>
        <fwb-table-cell>Laptop</fwb-table-cell>
        <fwb-table-cell>$2999</fwb-table-cell>
      </fwb-table-row>
      <fwb-table-row>
        <fwb-table-cell>
          <fwb-img
            alt="flowbite-vue"
            img-class="rounded-lg transition-all duration-300 cursor-pointer filter grayscale hover:grayscale-0"
            size="max-w-lg"
            src="./login.png"
          />
        </fwb-table-cell>
        <fwb-table-cell>White</fwb-table-cell>
        <fwb-table-cell>Laptop PC</fwb-table-cell>
        <fwb-table-cell>$1999</fwb-table-cell>
      </fwb-table-row>
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import { ref } from "vue/dist/vue.d.mts";
import {
  FwbButton,
  FwbCard,
  FwbInput,
  FwbFileInput,
  FwbA,
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
  FwbImg
} from "flowbite-vue";
import { useImageStore } from "@/store/modules/images";
import { useNotificationStore } from "@/store/modules/notifications";

const files = ref([]);
const loading = ref(false);
const store = useImageStore();
const notificationStore = useNotificationStore();

const saveFiles = async () => {
  if (files.value.length === 0) {
    notificationStore.showNotification(
      CONST.MESSAGES.VALIDATIONS.EMPTYFILES,
      "warning"
    );
    return;
  }

  const formData = new FormData();
  files.value.forEach(file => {
    formData.append("files[]", file);
  });

  try {
    loading.value = true;

    store.upload(formData).then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") router.push("/");
    });
  } catch (error) {
    notificationStore.showNotification(message, type);
  } finally {
    loading.value = false;
  }
};

</script>
