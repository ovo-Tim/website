import { createRouter, createWebHistory } from 'vue-router';
import MyProjects from '../views/MyProjects.vue';
import PersonalInfo from '../views/PersonalInfo.vue';
import ShellGame from '../views/ShellGame.vue';

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    {
      path: '/',
      name: 'home',
      component: PersonalInfo,
    },
    {
      path: '/projects',
      name: 'projects',
      component: MyProjects,
    },
    {
      path: '/game',
      name: 'game',
      component: ShellGame,
    },
  ],
});

export default router;
