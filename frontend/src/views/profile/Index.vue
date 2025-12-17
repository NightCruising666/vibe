<template>
  <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <p class="text-sm text-base-content/70">用户信息</p>
        <h2 class="text-2xl font-semibold">个人中心</h2>
      </div>
      <div class="badge badge-outline badge-primary">安全同步中</div>
    </div>
    <form class="mt-6 grid gap-5 md:grid-cols-2" @submit.prevent="save">
      <label class="form-control">
        <span class="label-text font-medium">姓名</span>
        <input v-model="form.full_name" class="input input-bordered" />
      </label>
      <label class="form-control">
        <span class="label-text font-medium">邮箱</span>
        <input v-model="form.email" type="email" class="input input-bordered" />
      </label>
      <label class="form-control md:col-span-2">
        <span class="label-text font-medium">电话</span>
        <input v-model="form.phone" class="input input-bordered" />
      </label>
      <div class="md:col-span-2 flex flex-wrap justify-end gap-3">
        <button type="button" class="btn btn-ghost" @click="load">重置</button>
        <button type="submit" class="btn btn-primary">保存</button>
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
