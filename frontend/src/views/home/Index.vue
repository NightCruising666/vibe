<template>
  <div class="space-y-6">
    <div class="rounded-3xl bg-gradient-to-r from-primary to-secondary p-8 text-primary-content shadow-lg">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="uppercase tracking-widest text-sm">Welcome Back</p>
          <h1 class="mt-2 text-3xl font-bold">学生信息管理驾驶舱</h1>
          <p class="mt-2 text-primary-content/80">
            快速浏览系统概况，查看近期更新，并在左侧导航进入具体模块。
          </p>
        </div>
        <div class="rounded-2xl bg-white/15 p-4 text-center">
          <p class="text-4xl font-bold">{{ summary.totalModules }}</p>
          <p class="text-sm uppercase tracking-wide">可用模块</p>
        </div>
      </div>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
        <p class="text-sm text-base-content/70">系统信息</p>
        <h2 class="text-2xl font-semibold">当前运行概况</h2>
        <dl class="mt-6 space-y-4">
          <div class="flex items-start justify-between">
            <dt class="text-base-content/70">系统版本</dt>
            <dd class="font-semibold">{{ info?.version || "N/A" }}</dd>
          </div>
          <div class="flex items-start justify-between">
            <dt class="text-base-content/70">最后更新</dt>
            <dd class="font-semibold">{{ info?.updated_at || "N/A" }}</dd>
          </div>
          <div class="flex items-start justify-between">
            <dt class="text-base-content/70">版权信息</dt>
            <dd class="text-right font-semibold">
              {{ info?.copyright || "学生信息管理系统" }}
            </dd>
          </div>
        </dl>
      </div>

      <div class="rounded-3xl bg-base-100 p-6 shadow-sm">
        <p class="text-sm text-base-content/70">快速引导</p>
        <h2 class="text-2xl font-semibold">常用操作</h2>
        <ul class="mt-6 space-y-3">
          <li v-for="item in shortcuts" :key="item.path" class="rounded-2xl border border-base-200 p-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold">{{ item.title }}</p>
                <p class="text-sm text-base-content/60">{{ item.desc }}</p>
              </div>
              <RouterLink :to="item.path" class="btn btn-outline btn-sm">进入</RouterLink>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import http from "@/api/http";

const info = ref(null);

const load = async () => {
  const res = await http.get("/home/info");
  info.value = res.data;
};

const shortcuts = [
  { title: "学生管理", desc: "维护学生档案与班级信息", path: "/students" },
  { title: "课程与成绩", desc: "录入课程与成绩数据", path: "/courses" },
  { title: "任务安排", desc: "跟踪待办任务与截止时间", path: "/tasks" },
  { title: "意见反馈", desc: "收集并回复用户反馈", path: "/feedback" },
];

const summary = computed(() => ({
  totalModules: 10,
}));

onMounted(load);
</script>
