import type { Config } from "tailwindcss"
import flowbite from "flowbite/plugin";

const config = {
  content: [
    "./index.html",
    "./src/main.ts",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    'node_modules/flowbite-vue/**/*.{js,jsx,ts,tsx,vue}',
    'node_modules/flowbite/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {
      borderRadius: {
        'l-lg': '0.5rem', // Ensure this matches what Flowbite expects
      },
    },
  },
  plugins: [
    flowbite
  ],
} satisfies Config

export default config