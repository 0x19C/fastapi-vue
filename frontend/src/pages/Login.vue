<template>
  <div class="login">
    <fwb-card img-alt="Desk" img-src="./login.png" variant="image">
      <div class="p-5 space-y-5">
        <fwb-input
          v-model="email"
          placeholder="enter your email"
          label="Email"
          size="lg"
          required
        />
        <fwb-input
          v-model="password"
          placeholder="enter your password"
          label="Password"
          size="lg"
          required
        />
        <fwb-button color="dark" size="lg" @click="login"> Login </fwb-button>
      </div>
    </fwb-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue/dist/vue.d.mts";
import { useRouter } from "vue-router";
import { FwbButton, FwbCard, FwbInput } from "flowbite-vue";
import { useUserStore } from "@/store/modules/users";

const router = useRouter();
const email = ref("");
const password = ref("");
const store = useUserStore();

function login() {
  store.login(email.value, password.value).then((_) => router.push("/"));
}
</script>

<style>
@media (min-width: 1024px) {
  .login {
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
