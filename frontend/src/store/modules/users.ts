import { ref, computed, onMounted } from "vue/dist/vue.d.mts";
import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";
import type { AlertType } from "flowbite-vue/components/FwbAlert/types.js";

interface User {
  username: string;
  email: string;
  token: string;
}

axios.defaults.withCredentials = true;

export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>({
    username: "Tester",
    email: "email",
    token: Cookies.get("Authorization") || "",
  });

  const username = computed(() => user.value?.username || null);
  const isLoggedIn = computed(() => !!user.value?.token);

  const setUser = (u: User | null) => {
    user.value = u;
  };

  const register = async (
    username: string,
    email: string,
    password: string
  ) => {
    return await axios
      .post(`${import.meta.env.VITE_API_ENDPOINT}/register`, {
        username,
        email,
        password,
      })
      .then((res) => {
        if (res.status === 200) {
          return {
            message: "You've successfully been registered. Welcome!",
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

  const login = async (email: string, password: string) => {
    const { data, message, type } = await axios
      .post(`${import.meta.env.VITE_API_ENDPOINT}/login`, {
        email,
        password,
      })
      .then((res) => {
        if (res.status === 200) {
          return {
            data: res.data as User,
            message: res.data.message,
            type: "success" as AlertType,
          };
        } else {
          return {
            data: null,
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
              data: null,
              message: detail,
              type: "warning" as AlertType,
            };
          }
          return {
            data: null,
            message: message,
            type: "danger" as AlertType,
          };
        }
      );
    const token = Cookies.get("Authorization") || "";
    setUser(
      data ? { email: data.email, username: data.username, token } : null
    );
    return { message, type };
  };

  const logout = async () => {
    const { message, type } = await axios
      .post(`${import.meta.env.VITE_API_ENDPOINT}/logout`)
      .then((res) => {
        return {
          message: res.data.message,
          type: "success" as AlertType,
        };
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
              data: null,
              message: detail,
              type: "warning" as AlertType,
            };
          }
          return {
            data: null,
            message: message,
            type: "danger" as AlertType,
          };
        }
      );
    setUser(null);
    return { message, type };
  };

  const whoami = async () => {
    const data = await axios
      .get(`${import.meta.env.VITE_API_ENDPOINT}/users/whoami`)
      .then((res) => {
        return res.data as User;
      })
      .catch((e) => {
        console.log(e);
        return null;
      });
    const token = Cookies.get("Authorization") || "";
    setUser(
      data ? { email: data.email, username: data.username, token } : null
    );
  };

  onMounted(() => {
    whoami();
  });

  return {
    user,
    username,
    isLoggedIn,
    setUser,
    register,
    login,
    whoami,
    logout,
  };
});
