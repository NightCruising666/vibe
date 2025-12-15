<template>
  <div class="card">
    <h2>首页</h2>
    <p v-if="info">版权信息：{{ info.copyright }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import http from "@/api/http";

const info = ref(null);

const load = async () => {
  const res = await http.get("/home/info");
  info.value = res.data;
};

onMounted(load);
</script>
