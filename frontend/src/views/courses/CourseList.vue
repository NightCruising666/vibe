<template>
  <div class="card">
    <h2>课程列表</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>课程名称</th>
          <th>学分</th>
          <th>描述</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.credit }}</td>
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
    <h3>{{ form.id ? "编辑课程" : "新增课程" }}</h3>
    <form @submit.prevent="submit">
      <label>
        课程名称
        <input v-model="form.name" required />
      </label>
      <label>
        学分
        <input v-model.number="form.credit" type="number" />
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
