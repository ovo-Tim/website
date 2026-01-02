import { createRouter, createWebHistory } from 'vue-router'
import PersonalInfo from '../views/PersonalInfo.vue'
import MyProjects from '../views/MyProjects.vue'

const router = createRouter({
    history: createWebHistory('/'),
    routes: [
        {
            path: '/',
            name: 'home',
            component: PersonalInfo
        },
        {
            path: '/projects',
            name: 'projects',
            component: MyProjects
        }
    ]
})

export default router