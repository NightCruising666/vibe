<template>
  <div class="card">
    <h2>学生信息列表</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>姓名</th>
          <th>性别</th>
          <th>生日</th>
          <th>班级</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.gender }}</td>
          <td>{{ item.birthday }}</td>
          <td>{{ item.class_name }}</td>
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
    <h3>{{ form.id ? "编辑学生" : "新增学生" }}</h3>
    <form @submit.prevent="submit">
      <label>
        姓名
        <input v-model="form.name" required />
      </label>
      <label>
        性别
        <select v-model="form.gender">
          <option value="">请选择</option>
          <option value="男">男</option>
          <option value="女">女</option>
        </select>
      </label>
      <label>
        生日
        <input v-model="form.birthday" type="date" />
      </label>
      <label>
        班级
        <select v-model="form.class_id">
          <option value="">请选择</option>
          <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
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
const classes = ref([]);
const form = reactive({
  id: null,
  name: "",
  gender: "",
  birthday: "",
  class_id: "",
});

const load = async () => {
  const res = await http.get("/students");
  items.value = res.data.items;
};

const loadClasses = async () => {
  const res = await http.get("/classes");
  classes.value = res.data.items;
};

const resetForm = () => {
  Object.assign(form, { id: null, name: "", gender: "", birthday: "", class_id: "" });
};

const edit = (item) => {
  Object.assign(form, { ...item });
};

const submit = async () => {
  const payload = { ...form };
  if (payload.class_id === "") payload.class_id = null;
  if (payload.id) {
    await http.put(`/students/${payload.id}`, payload);
  } else {
    await http.post("/students", payload);
  }
  await load();
  resetForm();
};

const remove = async (id) => {
  await http.delete(`/students/${id}`);
  await load();
};

onMounted(async () => {
  await Promise.all([load(), loadClasses()]);
});
</script>
