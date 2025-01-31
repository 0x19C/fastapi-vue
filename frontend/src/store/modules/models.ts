import { defineStore } from "pinia";
import axios from "axios";
import type { AlertType } from "flowbite-vue/components/FwbAlert/types.js";

interface Model {
  id: number;
  name: string;
}

axios.defaults.withCredentials = true;

export const useModelStore = defineStore("model", () => {
  const getList = async () => {
    return await axios
      .get(`${import.meta.env.VITE_API_ENDPOINT}/models`)
      .then((res) => {
        return res.data as Model[];
      })
      .catch((e) => {
        console.log(e);
        return null;
      });
  };

  const getDetail = async (id: number) => {
    return await axios
      .get(`${import.meta.env.VITE_API_ENDPOINT}/models/${id}`)
      .then((res) => {
        return res.data as Model;
      })
      .catch((e) => {
        console.log(e);
        return null;
      });
  };

  const store = async (
    name: string
  ) => {
    return await axios
      .post(`${import.meta.env.VITE_API_ENDPOINT}/models`,
        {
          name
        }
      )
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
      .delete(`${import.meta.env.VITE_API_ENDPOINT}/models/${id}`)
      .then((res) => {
        if (res.status === 200) {
          return {
            message: "You've successfully to delete models.",
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
    getDetail,
    store,
    destroy
  };
});
