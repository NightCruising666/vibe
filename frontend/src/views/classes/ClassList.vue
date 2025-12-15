<template>
  <div class="card">
    <h2>班级信息列表</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>班级名称</th>
          <th>年级</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.grade }}</td>
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
    <h3>{{ form.id ? "编辑班级" : "新增班级" }}</h3>
    <form @submit.prevent="submit">
      <label>
        班级名称
        <input v-model="form.name" required />
      </label>
      <label>
        年级
        <input v-model="form.grade" />
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
