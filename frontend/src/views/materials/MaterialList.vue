<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">资料库</p>
          <h2 class="text-2xl font-semibold">资料管理</h2>
        </div>
        <button class="btn btn-outline btn-sm" @click="load">刷新</button>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>标题</th>
              <th>描述</th>
              <th>文件</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.title }}</td>
              <td>{{ item.description || "-" }}</td>
              <td>
                <a
                  v-if="item.file_path"
                  :href="item.file_path"
                  target="_blank"
                  rel="noreferrer"
                  class="link link-primary"
                >
                  查看文件
                </a>
                <span v-else class="text-base-content/60">未上传</span>
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
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑资料" : "新增资料" }}</h3>
        <span v-if="form.id" class="badge badge-outline badge-info">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-2" @submit.prevent="submit">
        <label class="form-control">
          <span class="label-text font-medium">标题</span>
          <input v-model="form.title" class="input input-bordered" required />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">描述</span>
          <textarea v-model="form.description" rows="3" class="textarea textarea-bordered" />
        </label>
        <label class="form-control md:col-span-2">
          <span class="label-text font-medium">文件上传</span>
          <input type="file" class="file-input file-input-bordered w-full" @change="onFileChange" />
          <span v-if="form.file_path" class="label-text-alt text-success">已上传：{{ form.file_path }}</span>
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
const form = reactive({ id: null, title: "", description: "", file_path: "" });
const fileObj = ref(null);

const load = async () => {
  const res = await http.get("/materials");
  items.value = res.data.items;
};

const onFileChange = (e) => {
  fileObj.value = e.target.files[0];
};

const upload = async () => {
  if (!fileObj.value) return form.file_path;
  const fd = new FormData();
  fd.append("file", fileObj.value);
  const res = await http.post("/materials/upload", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data.file_path;
};

const edit = (item) => {
  Object.assign(form, { ...item });
  fileObj.value = null;
};

const reset = () => {
  Object.assign(form, { id: null, title: "", description: "", file_path: "" });
  fileObj.value = null;
};

const submit = async () => {
  const path = await upload();
  const payload = { ...form, file_path: path };
  if (form.id) {
    await http.put(`/materials/${form.id}`, payload);
  } else {
    await http.post("/materials", payload);
  }
  await load();
  reset();
};

const remove = async (id) => {
  await http.delete(`/materials/${id}`);
  await load();
};

onMounted(load);
</script>
