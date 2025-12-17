<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">系统管理</p>
          <h2 class="text-2xl font-semibold">管理员列表</h2>
        </div>
        <div class="flex gap-2">
          <button class="btn btn-outline btn-sm" @click="load">刷新</button>
          <button class="btn btn-primary btn-sm" @click="resetForm">新增管理员</button>
        </div>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>电话</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.username }}</td>
              <td>{{ item.name || "-" }}</td>
              <td>{{ item.email || "-" }}</td>
              <td>{{ item.phone || "-" }}</td>
              <td>
                <div class="flex justify-end gap-2">
                  <button class="btn btn-ghost btn-xs" @click="edit(item)">编辑</button>
                  <button class="btn btn-error btn-xs" @click="remove(item.id)">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑管理员" : "新增管理员" }}</h3>
        <span v-if="form.id" class="badge badge-outline badge-info">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-2" @submit.prevent="submit">
        <label class="form-control">
          <span class="label-text font-medium">用户名</span>
          <input v-model="form.username" class="input input-bordered" :disabled="!!form.id" required />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">密码</span>
          <input v-model="form.password" type="password" class="input input-bordered" :required="!form.id" />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">姓名</span>
          <input v-model="form.name" class="input input-bordered" />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">邮箱</span>
          <input v-model="form.email" class="input input-bordered" />
        </label>
        <label class="form-control md:col-span-2">
          <span class="label-text font-medium">电话</span>
          <input v-model="form.phone" class="input input-bordered" />
        </label>
        <div class="md:col-span-2 flex flex-wrap justify-end gap-3">
          <button type="button" class="btn btn-ghost" @click="resetForm">清空</button>
          <button type="submit" class="btn btn-primary">{{ form.id ? "保存修改" : "提交" }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import http from "@/api/http";

const items = ref([]);
const form = reactive({
  id: null,
  username: "",
  password: "",
  name: "",
  email: "",
  phone: "",
});

const load = async () => {
  const res = await http.get("/admins");
  items.value = res.data.items;
};

const resetForm = () => {
  Object.assign(form, { id: null, username: "", password: "", name: "", email: "", phone: "" });
};

const edit = (item) => {
  Object.assign(form, { ...item, password: "" });
};

const submit = async () => {
  if (form.id) {
    await http.put(`/admins/${form.id}`, form);
  } else {
    await http.post("/admins", form);
  }
  await load();
  resetForm();
};

const remove = async (id) => {
  await http.delete(`/admins/${id}`);
  await load();
};

onMounted(load);
</script>
