<template>
  <div class="card">
    <h2>个人中心</h2>
    <form @submit.prevent="save">
      <label>
        姓名
        <input v-model="form.full_name" />
      </label>
      <label>
        邮箱
        <input v-model="form.email" type="email" />
      </label>
      <label>
        电话
        <input v-model="form.phone" />
      </label>
      <div class="actions">
        <button type="submit">保存</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import http from "@/api/http";

const form = reactive({
  full_name: "",
  email: "",
  phone: "",
});

const load = async () => {
  const res = await http.get("/profile");
  Object.assign(form, res.data);
};

const save = async () => {
  await http.put("/profile", form);
  await load();
};

onMounted(load);
</script>
