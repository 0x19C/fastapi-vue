import { ref, computed } from "vue/dist/vue.d.mts";
import { defineStore } from "pinia";
import axios from "axios";

interface User {
  username: string;
  email: string;
  token: string;
}

export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>(null);

  const username = computed(() => user.value?.username || null)
  const isLoggedIn = computed(() => !!user.value?.token)

  function setUser(u: User | null) {
    user.value = u
  }

  async function login(email: string, password: string) {
    const data = await axios.post(`${import.meta.env.VITE_API_ENDPOINT}/login`, {
      email,
      password
    }).then((res) => {
      return res.data as User
    }).catch((e) => {
      console.log(e)
      return null
    })
    setUser(data)
  }

  return { user, username, isLoggedIn, setUser, login };
});
