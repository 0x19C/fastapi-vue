<template>
  <div class="px-6">
    <fwb-input
      v-model="name"
      placeholder="Model Name"
      label="Name"
      required
    />
    <fwb-button @click="saveModel" class="btn btn-primary mt-4">Save</fwb-button>
  </div>

  <div v-if="loading">Uploading...</div>

  <fwb-table class="mt-5">
    <fwb-table-head>
      <fwb-table-head-cell>id</fwb-table-head-cell>
      <fwb-table-head-cell>Name</fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body v-for="(data, index) in listData" :key="index">
      <fwb-table-row>
        <fwb-table-cell>{{ index + 1 }}</fwb-table-cell>
        <fwb-table-cell>{{ data.name }}</fwb-table-cell>
        <fwb-table-cell>
          <fwb-button @click="goDetail(data.id)" class="btn bg-blue-700">Detail</fwb-button>
          <fwb-button @click="destroy(data.id)" class="btn bg-red-700 ml-3">Delete</fwb-button>
        </fwb-table-cell>
      </fwb-table-row>
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue/dist/vue.d.mts";
import {
  FwbButton,
  FwbInput,
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
} from "flowbite-vue";
import { useModelStore } from "@/store/modules/models";
import { useNotificationStore } from "@/store/modules/notifications";
import { useRouter } from "vue-router";

const router = useRouter();
const listData = ref();
const name = ref("");
const loading = ref(false);
const store = useModelStore();
const notificationStore = useNotificationStore();

const fetchData = async () => {
  store.getList().then((res) => {
    listData.value = res;
  });
};

const goDetail = async (id: number) => {
  router.push(`/model/${id}`);
}

const saveModel = async () => {
  try {
    loading.value = true;

    store.store(name.value).then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") {
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
