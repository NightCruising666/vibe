<template>
  <div class="card">
    <h2>成绩信息列表</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>学生</th>
          <th>课程</th>
          <th>成绩</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.student_name }}</td>
          <td>{{ item.course_name }}</td>
          <td>{{ item.score }}</td>
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
    <h3>{{ form.id ? "编辑成绩" : "新增成绩" }}</h3>
    <form @submit.prevent="submit">
      <label>
        学生
        <select v-model="form.student_id" required>
          <option value="">请选择</option>
          <option v-for="s in students" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </label>
      <label>
        课程
        <select v-model="form.course_id" required>
          <option value="">请选择</option>
          <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </label>
      <label>
        成绩
        <input v-model.number="form.score" type="number" step="0.1" />
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
const students = ref([]);
const courses = ref([]);
const form = reactive({ id: null, student_id: "", course_id: "", score: "" });

const load = async () => {
  const res = await http.get("/scores");
  items.value = res.data.items;
};

const loadRefs = async () => {
  const [sRes, cRes] = await Promise.all([http.get("/students"), http.get("/courses")]);
  students.value = sRes.data.items;
  courses.value = cRes.data.items;
};

const edit = (item) => Object.assign(form, { ...item });
const reset = () => Object.assign(form, { id: null, student_id: "", course_id: "", score: "" });

const submit = async () => {
  if (form.id) {
    await http.put(`/scores/${form.id}`, form);
  } else {
    await http.post("/scores", form);
  }
  await load();
  reset();
};

const remove = async (id) => {
  await http.delete(`/scores/${id}`);
  await load();
};

onMounted(async () => {
  await Promise.all([load(), loadRefs()]);
});
</script>
