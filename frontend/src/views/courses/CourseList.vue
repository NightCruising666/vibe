<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">课程管理</p>
          <h2 class="text-2xl font-semibold">课程列表</h2>
        </div>
        <div class="flex gap-2">
          <button class="btn btn-outline btn-sm" @click="load">刷新</button>
          <button class="btn btn-primary btn-sm" @click="reset">新增课程</button>
        </div>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>课程名称</th>
              <th>学分</th>
              <th>描述</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>
                <span class="badge badge-outline badge-primary">{{ item.credit || 0 }} 学分</span>
              </td>
              <td>{{ item.description || "-" }}</td>
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
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑课程" : "新增课程" }}</h3>
        <span v-if="form.id" class="badge badge-outline badge-info">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-2" @submit.prevent="submit">
        <label class="form-control">
          <span class="label-text font-medium">课程名称</span>
          <input v-model="form.name" class="input input-bordered" required />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">学分</span>
          <input v-model.number="form.credit" type="number" class="input input-bordered" min="0" step="0.5" />
        </label>
        <label class="form-control md:col-span-2">
          <span class="label-text font-medium">描述</span>
          <textarea v-model="form.description" rows="3" class="textarea textarea-bordered" />
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
const form = reactive({ id: null, name: "", credit: "", description: "" });

const load = async () => {
  const res = await http.get("/courses");
  items.value = res.data.items;
};

const edit = (item) => Object.assign(form, { ...item });
const reset = () => Object.assign(form, { id: null, name: "", credit: "", description: "" });

const submit = async () => {
  if (form.id) {
    await http.put(`/courses/${form.id}`, form);
  } else {
    await http.post("/courses", form);
  }
  await load();
  reset();
};

const remove = async (id) => {
  await http.delete(`/courses/${id}`);
  await load();
};

onMounted(load);
</script>
