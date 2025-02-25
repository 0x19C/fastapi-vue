import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import './index.css'
// import '../node_modules/flowbite-vue/dist/index.css'

const app = createApp(App)

app.use(store)
app.use(router)
app.mount('#app')
