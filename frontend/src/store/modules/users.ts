import { ref, computed, onMounted } from "vue/dist/vue.d.mts";
import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

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

  function setUser(u: User | null) {
    user.value = u;
  }

  async function login(email: string, password: string) {
    const data = await axios
      .post(`${import.meta.env.VITE_API_ENDPOINT}/login`, {
        email,
        password,
      })
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
  }

  async function whoami() {
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
  }

  onMounted(() => {
    whoami();
  });

  return { user, username, isLoggedIn, setUser, login, whoami };
});
