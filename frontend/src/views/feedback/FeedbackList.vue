<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-sm text-base-content/70">用户反馈</p>
          <h2 class="text-2xl font-semibold">意见信息列表</h2>
        </div>
        <button class="btn btn-outline btn-sm" @click="load">刷新</button>
      </div>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-base-200">
        <table class="table">
          <thead class="bg-base-200 text-base-content/70">
            <tr>
              <th>ID</th>
              <th>内容</th>
              <th>联系方式</th>
              <th class="text-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td class="font-semibold">#{{ item.id }}</td>
              <td>{{ item.content }}</td>
              <td>{{ item.contact || "-" }}</td>
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
        <h3 class="text-xl font-semibold">{{ form.id ? "编辑意见" : "录入意见" }}</h3>
        <span v-if="form.id" class="badge badge-outline badge-info">ID #{{ form.id }}</span>
      </div>
      <form class="grid gap-5 md:grid-cols-2" @submit.prevent="submit">
        <label class="form-control md:col-span-2">
          <span class="label-text font-medium">反馈内容</span>
          <textarea v-model="form.content" rows="4" class="textarea textarea-bordered" required />
        </label>
        <label class="form-control md:col-span-2">
          <span class="label-text font-medium">联系方式</span>
          <input v-model="form.contact" class="input input-bordered" placeholder="邮箱或电话" />
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
