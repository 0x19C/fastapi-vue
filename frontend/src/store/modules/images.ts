import { defineStore } from "pinia";
import axios from "axios";
import type { AlertType } from "flowbite-vue/components/FwbAlert/types.js";

axios.defaults.withCredentials = true;

export const useImageStore = defineStore("image", () => {
  const upload = async (
    formData: FormData
  ) => {
    return await axios
      .post(`${import.meta.env.VITE_API_ENDPOINT}/datasets`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((res) => {
        if (res.status === 200) {
          return {
            message: "You've successfully created datasets.",
            type: "success" as AlertType,
          };
        } else {
          return {
            message: res.data.message,
            type: "warning" as AlertType,
          };
        }
      })
      .catch(
        ({
          status,
          message,
          response: {
            data: { detail },
          },
        }) => {
          if (status >= 400 && status < 500) {
            return {
              message: detail,
              type: "warning" as AlertType,
            };
          }
          return {
            message: message,
            type: "danger" as AlertType,
          };
        }
      );
  };

  return {
    upload,
  };
});
