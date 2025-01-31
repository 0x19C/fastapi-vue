<template>
  <fwb-navbar>
    <template #logo>
      <fwb-navbar-logo alt="Flowbite logo" image-url="/logo.svg" link="/">
        Flowbite
      </fwb-navbar-logo>
    </template>
    <template #default="{ isShowMenu }">
      <fwb-navbar-collapse v-if="isLoggedIn" :is-show-menu="isShowMenu">
        <fwb-navbar-link class="py-2" is-active link="#">
          Home
        </fwb-navbar-link>
        <fwb-navbar-link class="py-2" link="/dataset"> Dataset </fwb-navbar-link>
        <fwb-navbar-link class="py-2" link="/model"> Model </fwb-navbar-link>
        <fwb-navbar-link class="py-2" link="#"> Contact </fwb-navbar-link>
        <fwb-dropdown :text="username" align-to-end>
          <fwb-list-group class="w-20">
            <fwb-list-group-item>
              <fwb-navbar-link class="py-1" link="/register">
                Create a new Account
              </fwb-navbar-link>
            </fwb-list-group-item>
            <fwb-list-group-item>
              <span class="py-1 cursor-pointer" @click="() => logout()">
                Logout
              </span>
            </fwb-list-group-item>
          </fwb-list-group>
        </fwb-dropdown>
      </fwb-navbar-collapse>
      <fwb-navbar-collapse v-else :is-show-menu="isShowMenu">
        <fwb-a class="py-2" href="/register"> Register </fwb-a>
        <fwb-a class="py-2" href="/login"> Login </fwb-a>
      </fwb-navbar-collapse>
    </template>
  </fwb-navbar>
  <div v-if="isVisible" class="vp-raw grid gap-2 absolute right-10 w-4xs">
    <fwb-alert class="border-t-4 rounded-none" :type="messageType">
      <span>{{ messageTitle }}</span>
      <ul v-if="messageList.length" class="mt-1.5 ml-4 list-disc list-inside">
        <li v-for="message in messageList">{{ message }}</li>
      </ul>
    </fwb-alert>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue/dist/vue.d.mts";
import {
  FwbA,
  FwbAlert,
  FwbDropdown,
  FwbListGroup,
  FwbListGroupItem,
  FwbNavbar,
  FwbNavbarCollapse,
  FwbNavbarLink,
  FwbNavbarLogo,
} from "flowbite-vue";
import { useUserStore } from "@/store/modules/users";
import { useNotificationStore } from "@/store/modules/notifications";
import { useRouter } from "vue-router";

const router = useRouter();

const store = useUserStore();
const username = computed(() => store.username || "");
const isLoggedIn = computed(() => store.isLoggedIn);

const notificationStore = useNotificationStore();
const isVisible = computed(() => notificationStore.isVisible);
const messageType = computed(() => notificationStore.type);
const messageTitle = computed(() => notificationStore.title);
const messageList = computed(() => notificationStore.messages);

const logout = () => {
  store.logout().then(({ message, type }) => {
    notificationStore.showNotification(message, type);
    if (type == "success") router.push("/login");
  });
};
</script>
