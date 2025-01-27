<template>
  <div class="register">
    <fwb-card img-alt="Desk" img-src="./login.png" variant="image">
      <div class="p-5 space-y-5">
        <fwb-input
          v-model="username"
          placeholder="enter your username"
          label="Username"
          size="lg"
          required
        />
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
        <fwb-input
          v-model="confirmPassword"
          placeholder="enter your comfirm password"
          label="Confirm Password"
          size="lg"
          required
        />
        <fwb-button color="dark" size="lg" @click="register">
          Register
        </fwb-button>
      </div>
    </fwb-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue/dist/vue.d.mts";
import { useRouter } from "vue-router";
import { FwbButton, FwbCard, FwbInput } from "flowbite-vue";
import axios from "axios";

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

async function register() {
  if (password !== confirmPassword) {
  }
  const data = await axios
    .post(`${import.meta.env.VITE_API_ENDPOINT}/register`, {
      username,
      email,
      password,
    })
    .then((res) => {
      router.push("/login");
    })
    .catch((e) => {
      console.log(e);
      return null;
    });
}
</script>

<style>
@media (min-width: 1024px) {
  .register {
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
