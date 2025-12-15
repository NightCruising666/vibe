<template>
  <div class="card">
    <h2>意见信息列表</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>内容</th>
          <th>联系方式</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.content }}</td>
          <td>{{ item.contact }}</td>
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
    <h3>{{ form.id ? "编辑意见" : "录入意见" }}</h3>
    <form @submit.prevent="submit">
      <label>
        内容
        <textarea v-model="form.content" rows="3" required />
      </label>
      <label>
        联系方式
        <input v-model="form.contact" />
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
const form = reactive({ id: null, content: "", contact: "" });

const load = async () => {
  const res = await http.get("/feedback");
  items.value = res.data.items;
};

const edit = (item) => Object.assign(form, { ...item });
const reset = () => Object.assign(form, { id: null, content: "", contact: "" });

const submit = async () => {
  if (form.id) {
    await http.put(`/feedback/${form.id}`, form);
  } else {
    await http.post("/feedback", form);
  }
  await load();
  reset();
};

const remove = async (id) => {
  await http.delete(`/feedback/${id}`);
  await load();
};

onMounted(load);
</script>
