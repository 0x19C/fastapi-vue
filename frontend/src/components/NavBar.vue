<template>
  <fwb-navbar>
    <template #logo>
      <fwb-navbar-logo alt="Flowbite logo" image-url="/logo.svg" link="#">
        Flowbite
      </fwb-navbar-logo>
    </template>
    <template #default="{ isShowMenu }">
      <fwb-navbar-collapse v-if="isLoggedIn" :is-show-menu="isShowMenu">
        <fwb-navbar-link is-active link="#"> Home </fwb-navbar-link>
        <fwb-navbar-link link="#"> Services </fwb-navbar-link>
        <fwb-navbar-link link="#"> Pricing </fwb-navbar-link>
        <fwb-navbar-link link="#"> Contact </fwb-navbar-link>
      </fwb-navbar-collapse>
      <fwb-a v-else href="/login"> Login </fwb-a>
    </template>
  </fwb-navbar>
</template>

<script setup>
import { computed } from "vue/dist/vue.d.mts";
import {
  FwbNavbar,
  FwbNavbarCollapse,
  FwbNavbarLink,
  FwbNavbarLogo,
  FwbA
} from "flowbite-vue";
import { useUserStore } from "@/store/modules/users";

const store = useUserStore();
const token = computed(() => store.token);
const isLoggedIn = computed(() => store.isLoggedIn);

function logout() {
  store.setUser(null);
}
</script>
