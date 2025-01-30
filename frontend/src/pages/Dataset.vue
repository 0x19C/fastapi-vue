<template>
  <div class="px-6">
    <fwb-file-input 
      v-model="files" 
      label="Choose files"
      multiple
      required
      accept="image/*, .zip"
    />
    <fwb-input
      v-model="name"
      placeholder="Dataset Name"
      label="Name"
      required
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
      <fwb-table-head-cell>Images</fwb-table-head-cell>
      <fwb-table-head-cell>Name</fwb-table-head-cell>
      <fwb-table-head-cell>Sample Count</fwb-table-head-cell>
      <fwb-table-head-cell>Action</fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body v-for="(data, index) in listData" :key="index">
      <fwb-table-row>
        <fwb-table-cell :style="{ width: '40%' }">
          <fwb-carousel :pictures="transformImages(data.dataset_images)" />
        </fwb-table-cell>
        <fwb-table-cell>{{ data.name }}</fwb-table-cell>
        <fwb-table-cell>{{ data.sample_count }}</fwb-table-cell>
        <fwb-table-cell>
          <fwb-button @click="detailModal" class="btn bg-blue-700">Detail</fwb-button>
          <fwb-button @click="destroy(data.id)" class="btn bg-red-700 ml-3">Delete</fwb-button>
        </fwb-table-cell>
      </fwb-table-row>
    </fwb-table-body>
  </fwb-table>
  <fwb-modal v-if="isModalOpen" size="5xl" @close="closeModal">
    <template #header>
      <h3 class="text-lg font-semibold">Modal Title</h3>
    </template>
    <template #body>
      <p>This is the content inside the modal.</p>
    </template>
    <template #footer>
      <fwb-button @click="closeModal">Close</fwb-button>
    </template>
  </fwb-modal>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import {
  FwbButton,
  FwbInput,
  FwbFileInput,
  FwbModal,
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
  FwbCarousel
} from "flowbite-vue";
import { useImageStore } from "@/store/modules/images";
import { useNotificationStore } from "@/store/modules/notifications";
import CONST from "@/utils/consts";

const listData = ref();
const files = ref([]);
const name = ref("");
const loading = ref(false);
const isModalOpen = ref(false);
const store = useImageStore();
const notificationStore = useNotificationStore();

const pictures = [
  {src: '/login.png'},
  {src: '/login.png'},
  {src: '/login.png'},
];

const detailModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const transformImages = (images) => {
  return images.map(item => ({
    src: `${import.meta.env.VITE_API_ENDPOINT}/${item.file_path}`
  }));
}

const fetchData = async () => {
  store.getList().then((res) => {
    listData.value = res;
  });
};

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
    formData.append("files", file);
  });
  formData.append('name', name.value);

  try {
    loading.value = true;

    store.upload(formData).then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") {
        files.value = [];
        name.value = "";
        fetchData();
      }
    });
  } catch (error) {
    console.log(error);
  } finally {
    loading.value = false;
  }
};

const destroy = async (id: number) => {
  try {
    loading.value = true;

    store.destroy(id).then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") fetchData();
    });
  } catch (error) {
    console.log(error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});

</script>
