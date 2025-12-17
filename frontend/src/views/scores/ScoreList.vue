<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">成绩管理</p>
          <h2 class="text-2xl font-semibold">成绩信息列表</h2>
        </div>
        <button class="btn btn-outline btn-sm" @click="load">刷新</button>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>学生</th>
              <th>课程</th>
              <th>成绩</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.student_name }}</td>
              <td>{{ item.course_name }}</td>
              <td>
                <span class="badge badge-outline badge-primary">{{ item.score ?? "-" }}</span>
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
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑成绩" : "新增成绩" }}</h3>
        <span v-if="form.id" class="badge badge-outline badge-info">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-3" @submit.prevent="submit">
        <label class="form-control md:col-span-1">
          <span class="label-text font-medium">学生</span>
          <select v-model="form.student_id" class="select select-bordered" required>
            <option value="">请选择</option>
            <option v-for="s in students" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </label>
        <label class="form-control md:col-span-1">
          <span class="label-text font-medium">课程</span>
          <select v-model="form.course_id" class="select select-bordered" required>
            <option value="">请选择</option>
            <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </label>
        <label class="form-control md:col-span-1">
          <span class="label-text font-medium">成绩</span>
          <input v-model.number="form.score" type="number" step="0.1" class="input input-bordered" />
        </label>
        <div class="md:col-span-3">
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
