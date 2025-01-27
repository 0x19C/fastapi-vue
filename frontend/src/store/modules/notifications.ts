import { ref } from "vue/dist/vue.d.mts";
import { defineStore } from "pinia";
import type { AlertType } from "flowbite-vue/components/FwbAlert/types.js";

export const useNotificationStore = defineStore("notification", () => {
  const title = ref("");
  const type = ref<AlertType>("dark");
  const isVisible = ref(false);
  const messages = ref<string[]>([]);

  const clearNotification = () => {
    isVisible.value = false;
    title.value = "";
    type.value = "dark";
    messages.value = [];
  };

  // Function to show a notification
  const showNotification = (
    t: string,
    notificationType: AlertType,
    msgs: string[] = []
  ) => {
    title.value = t;
    type.value = notificationType;
    isVisible.value = true;
    messages.value = msgs;

    // Hide the notification after 5 seconds
    setTimeout(clearNotification, 5000); // 5 seconds lifecycle
  };

  return {
    title,
    type,
    isVisible,
    messages,
    showNotification,
    clearNotification,
  };
});
