<template>
  <div class="flex min-h-screen bg-base-200 text-base-content">
    <aside class="hidden w-72 flex-col border-r border-base-300 bg-base-100 p-6 lg:flex">
      <div class="flex items-center gap-3 pb-8">
        <div class="rounded-2xl bg-primary/10 p-3 text-primary">
          <span class="text-xl font-bold">SM</span>
        </div>
        <div>
          <p class="text-sm text-base-content/60">Student Portal</p>
          <p class="text-lg font-semibold">学生信息管理</p>
        </div>
      </div>
      <nav class="flex-1">
        <ul class="menu menu-lg gap-1 rounded-box bg-base-100 p-0">
          <li v-for="item in navItems" :key="item.path">
            <RouterLink
              :to="item.path"
              :class="['rounded-xl', isActive(item.path) ? 'bg-primary/10 text-primary' : '']"
            >
              <span class="text-base">{{ item.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </nav>
      <div class="mt-6 rounded-2xl bg-base-200 p-4">
        <p class="text-sm text-base-content/60">账号安全</p>
        <p class="mt-1 text-base">请妥善保管管理员账号</p>
      </div>
    </aside>

    <div class="flex flex-1 flex-col">
      <header class="navbar border-b border-base-300 bg-base-100 px-4 lg:px-8">
        <div class="flex flex-1 items-center gap-3">
          <button class="btn btn-ghost lg:hidden" @click="toggleDrawer">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div>
            <p class="text-xs uppercase tracking-wide text-base-content/60">Dashboard</p>
            <p class="text-lg font-semibold">学生信息管理系统</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button class="btn btn-sm btn-ghost" @click="refreshRoute">
            刷新
          </button>
          <button class="btn btn-sm btn-primary" @click="logout">退出登录</button>
        </div>
      </header>

      <section class="flex-1 overflow-y-auto p-4 lg:p-8">
        <div class="mx-auto max-w-6xl space-y-6">
          <RouterView />
        </div>
      </section>
    </div>

    <Transition name="fade">
      <div
        v-if="showMobileNav"
        class="fixed inset-0 z-50 flex lg:hidden"
        @click.self="toggleDrawer"
      >
        <div class="w-72 bg-base-100 p-6 shadow-2xl">
          <div class="flex items-center justify-between">
            <p class="text-lg font-semibold">导航菜单</p>
            <button class="btn btn-sm btn-ghost" @click="toggleDrawer">关闭</button>
          </div>
          <ul class="menu mt-6 gap-1 rounded-box bg-base-100 p-0">
            <li v-for="item in navItems" :key="`mobile-${item.path}`">
              <RouterLink
                :to="item.path"
                @click="toggleDrawer"
                :class="['rounded-xl', isActive(item.path) ? 'bg-primary/10 text-primary' : '']"
              >
                {{ item.label }}
              </RouterLink>
            </li>
          </ul>
        </div>
        <div class="flex-1 bg-black/40" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter, RouterLink, RouterView } from "vue-router";
import http from "./api/http";

const route = useRoute();
const router = useRouter();
const showMobileNav = ref(false);

const navItems = [
  { label: "首页", path: "/home" },
  { label: "个人中心", path: "/profile" },
  { label: "系统管理", path: "/system/admins" },
  { label: "学生管理", path: "/students" },
  { label: "班级管理", path: "/classes" },
  { label: "成绩管理", path: "/scores" },
  { label: "课程管理", path: "/courses" },
  { label: "任务管理", path: "/tasks" },
  { label: "资料管理", path: "/materials" },
  { label: "意见反馈", path: "/feedback" },
];

const isActive = (path) => route.path.startsWith(path);

const logout = async () => {
  try {
    await http.post("/auth/logout");
  } catch (e) {
    console.warn(e);
  } finally {
    router.push("/home");
  }
};

const refreshRoute = () => {
  router.go(0);
};

const toggleDrawer = () => {
  showMobileNav.value = !showMobileNav.value;
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
