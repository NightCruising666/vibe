<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">学生管理</p>
          <h2 class="text-2xl font-semibold">学生信息列表</h2>
        </div>
        <div class="flex flex-wrap gap-2">
          <button class="btn btn-outline btn-sm" @click="load">刷新</button>
          <button class="btn btn-primary btn-sm" @click="resetForm">新增学生</button>
        </div>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>性别</th>
              <th>生日</th>
              <th>班级</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>
                <span class="badge badge-outline badge-primary uppercase">{{ item.gender || "未填写" }}</span>
              </td>
              <td>{{ item.birthday || "-" }}</td>
              <td>{{ item.class_name || "-" }}</td>
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
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑学生" : "新增学生" }}</h3>
        <span v-if="form.id" class="badge badge-info badge-outline">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-2" @submit.prevent="submit">
        <label class="form-control">
          <span class="label-text font-medium">姓名</span>
          <input v-model="form.name" class="input input-bordered" required />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">性别</span>
          <select v-model="form.gender" class="select select-bordered">
            <option value="">请选择</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </label>
        <label class="form-control">
          <span class="label-text font-medium">Birthday</span>
          <input
            id="student-birthday"
            v-model="form.birthday"
            type="date"
            placeholder="yyyy-mm-dd"
            class="input input-bordered"
          />
        </label>
        <label class="form-control">
          <span class="label-text font-medium">班级</span>
          <select v-model="form.class_id" class="select select-bordered">
            <option value="">请选择</option>
            <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
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
