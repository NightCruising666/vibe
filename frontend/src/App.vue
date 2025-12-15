<template>
  <div class="layout">
    <aside class="sidebar">
      <h1>学生信息管理</h1>
      <nav>
        <RouterLink class="nav-link" :class="{ active: isActive('/home') }" to="/home">首页</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/profile') }" to="/profile">个人中心</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/system/admins') }" to="/system/admins">系统管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/students') }" to="/students">学生管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/classes') }" to="/classes">班级管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/scores') }" to="/scores">成绩管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/courses') }" to="/courses">课程管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/tasks') }" to="/tasks">任务管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/materials') }" to="/materials">资料管理</RouterLink>
        <RouterLink class="nav-link" :class="{ active: isActive('/feedback') }" to="/feedback">意见反馈</RouterLink>
      </nav>
    </aside>
    <main class="main">
      <header class="topbar">
        <div>欢迎来到学生信息管理系统</div>
        <div class="actions">
          <button class="secondary" @click="logout">退出登录</button>
        </div>
      </header>
      <section class="content">
        <RouterView />
      </section>
    </main>
  </div>
</template>

<script setup>
import { useRoute, useRouter, RouterLink, RouterView } from "vue-router";
import http from "./api/http";

const route = useRoute();
const router = useRouter();

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
</script>
