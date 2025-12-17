<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">教学班级</p>
          <h2 class="text-2xl font-semibold">班级信息列表</h2>
        </div>
        <button class="btn btn-outline btn-sm" @click="load">刷新</button>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>班级名称</th>
              <th>年级</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>
                <span class="badge badge-outline badge-secondary">{{ item.grade || "未设置" }}</span>
              </td>
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
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑班级" : "新增班级" }}</h3>
        <span v-if="form.id" class="badge badge-outline badge-info">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-2" @submit.prevent="submit">
        <label class="form-control">
          <span class="label-text font-medium">班级名称</span>
          <input v-model="form.name" class="input input-bordered" required />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">年级</span>
          <input v-model="form.grade" class="input input-bordered" />
        </label>
        <div class="md:col-span-2">
          <button type="submit" class="btn btn-primary w-full md:w-auto">
            {{ form.id ? "保存修改" : "提交" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import http from "@/api/http";

const items = ref([]);
const form = reactive({ id: null, name: "", grade: "" });

const load = async () => {
  const res = await http.get("/classes");
  items.value = res.data.items;
};

const edit = (item) => Object.assign(form, { ...item });
const reset = () => Object.assign(form, { id: null, name: "", grade: "" });

const submit = async () => {
  if (form.id) {
    await http.put(`/classes/${form.id}`, form);
  } else {
    await http.post("/classes", form);
  }
  await load();
  reset();
};

const remove = async (id) => {
  await http.delete(`/classes/${id}`);
  await load();
};

onMounted(load);
</script>
