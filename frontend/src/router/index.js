import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/home/Index.vue";
import Profile from "@/views/profile/Index.vue";
import AdminList from "@/views/system/AdminList.vue";
import StudentList from "@/views/students/StudentList.vue";
import ClassList from "@/views/classes/ClassList.vue";
import CourseList from "@/views/courses/CourseList.vue";
import ScoreList from "@/views/scores/ScoreList.vue";
import TaskList from "@/views/tasks/TaskList.vue";
import MaterialList from "@/views/materials/MaterialList.vue";
import FeedbackList from "@/views/feedback/FeedbackList.vue";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: Home },
  { path: "/profile", component: Profile },
  { path: "/system/admins", component: AdminList },
  { path: "/students", component: StudentList },
  { path: "/classes", component: ClassList },
  { path: "/courses", component: CourseList },
  { path: "/scores", component: ScoreList },
  { path: "/tasks", component: TaskList },
  { path: "/materials", component: MaterialList },
  { path: "/feedback", component: FeedbackList },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
