import { defineStore } from "pinia";
import axios from "axios";
import type { AlertType } from "flowbite-vue/components/FwbAlert/types.js";

interface Image {
  id: number;
  name: string;
  file_path: string;
  metadata: {}
}

interface DataSet {
  id: number;
  name: string;
  directory_path: string;
  dataset_images: Image[]
}

axios.defaults.withCredentials = true;

export const useImageStore = defineStore("image", () => {
  const getList = async () => {
    return await axios
      .get(`${import.meta.env.VITE_API_ENDPOINT}/datasets`)
      .then((res) => {
        return res.data as DataSet[];
      })
      .catch((e) => {
        console.log(e);
        return null;
      });
  };

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

  const destroy = async (
    id: number
  ) => {
    return await axios
      .delete(`${import.meta.env.VITE_API_ENDPOINT}/datasets/${id}`)
      .then((res) => {
        if (res.status === 200) {
          return {
            message: "You've successfully to delete datasets.",
            type: "success" as AlertType,
          };
        } else {
          return {
            message: "You've failed to delete",
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
    getList,
    upload,
    destroy
  };
});
