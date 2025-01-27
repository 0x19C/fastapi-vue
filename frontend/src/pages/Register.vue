<template>
  <div class="min-h-[500px] flex items-center justify-center">
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
          type="password"
          required
        />
        <fwb-input
          v-model="confirmPassword"
          placeholder="enter your comfirm password"
          label="Confirm Password"
          size="lg"
          type="password"
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
import { useNotificationStore } from "@/store/modules/notifications";
import { useUserStore } from "@/store/modules/users";
import { isValidEmail, isStrongPassword } from "@/utils/validations";
import CONST from "@/utils/consts";

axios.defaults.withCredentials = true;

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const store = useUserStore();
const notificationStore = useNotificationStore();

const register = () => {
  if (!isValidEmail(email.value)) {
    notificationStore.showNotification(
      CONST.MESSAGES.VALIDATIONS.INVALIDEMAIL,
      "warning"
    );
    return;
  }
  if (!isStrongPassword(password.value)) {
    notificationStore.showNotification(
      CONST.MESSAGES.VALIDATIONS.NOTSTRONGPASSWORD,
      "warning",
      CONST.MESSAGES.VALIDATIONS.NOTSTRONGPASSWORDDETAILS
    );
    return;
  }
  if (password.value !== confirmPassword.value) {
    notificationStore.showNotification(
      CONST.MESSAGES.VALIDATIONS.PASSWORDNOTMATCHED,
      "warning"
    );
    return;
  }

  store
    .register(username.value, email.value, password.value)
    .then(({ message, type }) => {
      notificationStore.showNotification(message, type);
      if (type == "success") router.push("/login");
    });
};
</script>
