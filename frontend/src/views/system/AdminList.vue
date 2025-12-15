<template>
  <div class="card">
    <h2>管理员列表</h2>
    <div class="actions">
      <button @click="resetForm">新增管理员</button>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>姓名</th>
          <th>邮箱</th>
          <th>电话</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.email }}</td>
          <td>{{ item.phone }}</td>
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
    <h3>{{ form.id ? "编辑管理员" : "新增管理员" }}</h3>
    <form @submit.prevent="submit">
      <label>
        用户名
        <input v-model="form.username" :disabled="!!form.id" required />
      </label>
      <label>
        密码
        <input v-model="form.password" type="password" :required="!form.id" />
      </label>
      <label>
        姓名
        <input v-model="form.name" />
      </label>
      <label>
        邮箱
        <input v-model="form.email" />
      </label>
      <label>
        电话
        <input v-model="form.phone" />
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
