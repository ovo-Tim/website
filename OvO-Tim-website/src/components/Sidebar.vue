<script setup lang="ts">
import { RouterLink } from 'vue-router'

// We receive the collapsed state from the parent (App.vue)
defineProps<{
    isCollapsed: boolean
}>()
</script>

<template>
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
        <!-- Top: Avatar -->
        <div class="sidebar-top">
            <div class="avatar-container">
                <!-- Placeholder image - replace with your actual photo -->
                <img src="../assets/Mascot_konqi-app-dev.png" alt="Avatar" />
            </div>
            <h3 v-if="!isCollapsed" class="fade-in">OvO-Tim</h3>
        </div>

        <!-- Middle: Navigation -->
        <nav class="sidebar-nav">
            <RouterLink to="/" class="nav-item">
                <span class="icon">🏠</span>
                <span v-if="!isCollapsed" class="label">Personal Info</span>
            </RouterLink>
            <RouterLink to="/projects" class="nav-item">
                <span class="icon">🚀</span>
                <span v-if="!isCollapsed" class="label">My Projects</span>
            </RouterLink>
        </nav>

        <!-- Bottom: Social Links -->
        <div class="sidebar-footer">
            <a href="https://github.com/ovo-Tim/" target="_blank" class="social-link" title="GitHub">
                <span class="icon">🐙</span>
                <span v-if="!isCollapsed" class="label">GitHub</span>
            </a>
            <a href="https://mastodon.social" target="_blank" class="social-link" title="Mastodon">
                <span class="icon">🐘</span>
                <span v-if="!isCollapsed" class="label">Mastodon</span>
            </a>
        </div>
    </aside>
</template>

<style scoped>
.sidebar {
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    height: 100vh;
    width: 260px;
    padding: 1.5rem;
    /* The 3D Shadow */
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.05);
    transition: width 0.3s ease, padding 0.3s ease;
    z-index: 10;
}

.sidebar.collapsed {
    width: 80px;
    padding: 1.5rem 0.5rem;
    align-items: center;
}

/* Top Section */
.sidebar-top {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 2rem;
}

.avatar-container img {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: width 0.3s;
}

.collapsed .avatar-container img {
    width: 40px;
    height: 40px;
}

h3 {
    margin-top: 1rem;
    font-weight: 600;
    color: #333;
    white-space: nowrap;
}

/* Navigation */
.sidebar-nav {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    color: #555;
    text-decoration: none;
    border-radius: 12px;
    transition: all 0.2s ease;
}

.nav-item:hover,
.nav-item.router-link-active {
    background-color: #f0f4f8;
    color: #2c3e50;
    box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.05), inset -2px -2px 5px #fff;
    font-weight: bold;
}

.collapsed .nav-item {
    justify-content: center;
    padding: 0.75rem;
}

/* Footer */
.sidebar-footer {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    border-top: 1px solid #eee;
    padding-top: 1rem;
}

.social-link {
    display: flex;
    align-items: center;
    color: #666;
    text-decoration: none;
    padding: 0.5rem;
    border-radius: 8px;
    transition: background 0.2s;
}

.social-link:hover {
    background-color: #f9f9f9;
}

.collapsed .social-link {
    justify-content: center;
}

.icon {
    font-size: 1.2rem;
}

.label {
    margin-left: 10px;
}

/* Helper for hiding text smoothly */
.fade-in {
    animation: fadeIn 0.4s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
</style>