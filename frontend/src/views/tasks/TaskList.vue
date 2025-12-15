<template>
  <div class="card">
    <h2>任务信息列表</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>截止日期</th>
          <th>描述</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.due_date }}</td>
          <td>{{ item.description }}</td>
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
    <h3>{{ form.id ? "编辑任务" : "新增任务" }}</h3>
    <form @submit.prevent="submit">
      <label>
        标题
        <input v-model="form.title" required />
      </label>
      <label>
        截止日期
        <input v-model="form.due_date" type="date" />
      </label>
      <label>
        描述
        <textarea v-model="form.description" rows="3" />
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
const form = reactive({ id: null, title: "", due_date: "", description: "" });

const load = async () => {
  const res = await http.get("/tasks");
  items.value = res.data.items;
};

const edit = (item) => Object.assign(form, { ...item });
const reset = () => Object.assign(form, { id: null, title: "", due_date: "", description: "" });

const submit = async () => {
  if (form.id) {
    await http.put(`/tasks/${form.id}`, form);
  } else {
    await http.post("/tasks", form);
  }
  await load();
  reset();
};

const remove = async (id) => {
  await http.delete(`/tasks/${id}`);
  await load();
};

onMounted(load);
</script>
