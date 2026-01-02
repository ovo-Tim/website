<script setup lang="ts">
import { RouterLink } from 'vue-router';

// We receive the collapsed state and theme from the parent (App.vue)
defineProps<{
  isCollapsed: boolean;
  isDark: boolean;
}>();

defineEmits(['toggle-theme']);
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
            <RouterLink to="/game" class="nav-item">
                <span class="icon">🎮</span>
                <span v-if="!isCollapsed" class="label">Know Me More</span>
            </RouterLink>
        </nav>

        <!-- Bottom: Social Links -->
        <div class="sidebar-footer">
            <a href="https://github.com/ovo-Tim/" target="_blank" class="social-link" title="GitHub">
                <span class="icon">🐙</span>
                <span v-if="!isCollapsed" class="label">GitHub</span>
            </a>
            <a href="https://woof.tech/@TimTu" target="_blank" class="social-link" title="Mastodon">
                <span class="icon">🐘</span>
                <span v-if="!isCollapsed" class="label">Mastodon</span>
            </a>
            
            <button @click="$emit('toggle-theme')" class="theme-toggle" :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
                <span class="icon">{{ isDark ? '☀️' : '🌙' }}</span>
                <span v-if="!isCollapsed" class="label">{{ isDark ? 'Light Mode' : 'Dark Mode' }}</span>
            </button>
        </div>
    </aside>
</template>

<style scoped>
.sidebar {
    display: flex;
    flex-direction: column;
    background-color: var(--bg-sidebar);
    height: 100vh;
    width: 260px;
    padding: 1.5rem;
    box-shadow: var(--sidebar-shadow);
    transition: width 0.3s ease, padding 0.3s ease, background-color 0.3s ease;
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
    color: var(--text-primary);
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
    color: var(--text-secondary);
    text-decoration: none;
    border-radius: 12px;
    transition: all 0.2s ease;
}

.nav-item:hover,
.nav-item.router-link-active {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.05), inset -2px -2px 5px rgba(255, 255, 255, 0.1);
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
    border-top: 1px solid var(--divider-color);
    padding-top: 1rem;
}

.social-link, .theme-toggle {
    display: flex;
    align-items: center;
    color: var(--text-secondary);
    text-decoration: none;
    padding: 0.5rem;
    border-radius: 8px;
    transition: all 0.2s;
    background: transparent;
    border: none;
    cursor: pointer;
    width: 100%;
    text-align: left;
    font-size: inherit;
    font-family: inherit;
}

.social-link:hover, .theme-toggle:hover {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
}

.collapsed .social-link, .collapsed .theme-toggle {
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