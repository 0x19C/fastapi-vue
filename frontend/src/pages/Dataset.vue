<template>
  <fwb-button @click="showModal">
    Create
  </fwb-button>

  <fwb-modal v-if="isShowModal" @close="closeModal">
    <template #header>
      <div class="flex items-center text-lg">
        Create Dataset
      </div>
    </template>
    <template #body>
      <div class="grid gap-4 mb-4 grid-cols-2">
        <div class="col-span-2">
          <fwb-input
            v-model="name"
            placeholder="Dataset Name"
            label="Name"
            required
          />
        </div>
        <div class="col-span-2">
          <fwb-file-input 
            v-model="files" 
            label="Choose files"
            multiple
            required
            accept="image/*, .zip"
          />
          <div v-if="files.length !== 0" class="mt-4 border-[1px] border-gray-300 dark:border-gray-600 p-2 rounded-md">
            <div v-for="file in files" :key="file.name">
              {{ file.name }}
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-between">
        <fwb-button @click="closeModal" color="alternative">
          Cancel
        </fwb-button>
        <fwb-button @click="saveFiles" color="green">Save</fwb-button>
      </div>
    </template>
  </fwb-modal>

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
          <fwb-dropdown placement="bottom" text="Action">
            <nav class="py-2 text-sm text-gray-700 dark:text-gray-200">
              <a @click="goDetail(data.id)" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Detail</a>
              <a @click="destroy(data.id)" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Delete</a>
            </nav>
          </fwb-dropdown>
        </fwb-table-cell>
      </fwb-table-row>
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import { initFlowbite } from "flowbite";
import {
  FwbButton,
  FwbInput,
  FwbFileInput,
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
  FwbCarousel,
  FwbDropdown,
  FwbModal
} from "flowbite-vue";
import { useImageStore } from "@/store/modules/images";
import { useNotificationStore } from "@/store/modules/notifications";
import CONST from "@/utils/consts";
import { useRouter } from "vue-router";

const router = useRouter();
const listData = ref();
const files = ref<File[]>([]);
const name = ref("");
const loading = ref(false);
const store = useImageStore();
const notificationStore = useNotificationStore();
const isShowModal = ref(false);

const goDetail = async (id: number) => {
  router.push(`/dataset/${id}`);
}

const transformImages = (images: {file_path: string}[]) => {
  return images.map(item => ({
    src: `${import.meta.env.VITE_API_ENDPOINT}/${item.file_path}`
  }));
}

const fetchData = async () => {
  store.getList().then((res) => {
    listData.value = res;
  });
};

const closeModal = () => {
  isShowModal.value = false
};
const showModal = () => {
  isShowModal.value = true
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
        closeModal();
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
  initFlowbite();
  fetchData();
});

</script>
