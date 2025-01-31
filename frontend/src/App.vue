<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div>
    <NavBar />
    <div class="container mt-24">
      <router-view/>
    </div>
  </div>
</template>
