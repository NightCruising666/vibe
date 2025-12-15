<template>
  <div class="card">
    <h2>资料管理</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>描述</th>
          <th>文件</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.description }}</td>
          <td>
            <a v-if="item.file_path" :href="item.file_path" target="_blank" rel="noreferrer">查看</a>
          </td>
          <td>
            <div class="actions">
              <button class="secondary" @click="edit(item)">编辑</button>
              <button class="danger" @click="remove(item.id)">删除</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="card">
    <h3>{{ form.id ? "编辑资料" : "新增资料" }}</h3>
    <form @submit.prevent="submit">
      <label>
        标题
        <input v-model="form.title" required />
      </label>
      <label>
        描述
        <textarea v-model="form.description" rows="3" />
      </label>
      <label>
        文件
        <input type="file" @change="onFileChange" />
        <span v-if="form.file_path">已上传：{{ form.file_path }}</span>
      </label>
      <div class="actions">
        <button type="submit">提交</button>
      </div>
    </form>
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
