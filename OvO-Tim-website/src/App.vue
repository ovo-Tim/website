<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'

const isCollapsed = ref(false)
const isDark = ref(false)

// Function to check window width and adjust state
const checkScreenSize = () => {
	// Collapse sidebar if screen is narrower than 1024px
	isCollapsed.value = window.innerWidth < 1024
}

const toggleTheme = () => {
	isDark.value = !isDark.value
	localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
	updateThemeClass()
}

const updateThemeClass = () => {
	if (isDark.value) {
		document.documentElement.classList.add('dark')
	} else {
		document.documentElement.classList.remove('dark')
	}
}

// Set up listeners when the app loads
onMounted(() => {
	checkScreenSize()
	window.addEventListener('resize', checkScreenSize)
	
	const savedTheme = localStorage.getItem('theme')
	if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
		isDark.value = true
	}
	updateThemeClass()
})

// Clean up listeners when the app closes
onUnmounted(() => {
	window.removeEventListener('resize', checkScreenSize)
})
</script>

<template>
	<div class="app-layout" :class="{ 'dark-mode': isDark }">
		<!-- Navigation Left -->
		<Sidebar :isCollapsed="isCollapsed" :isDark="isDark" @toggle-theme="toggleTheme" />

		<!-- Main Content Right -->
		<main class="main-content">
			<!--
        RouterView is where the specific page content
        (PersonalInfo or MyProjects) will appear
      -->
			<RouterView v-slot="{ Component }">
				<transition name="fade" mode="out-in">
					<component :is="Component" />
				</transition>
			</RouterView>
		</main>
	</div>
</template>

<style>
/* Global Resets & Theme Variables */
:root {
	/* Light Theme Colors */
	--bg-primary: #f8fafc;
	--bg-secondary: #f1f5f9;
	--bg-sidebar: #ffffff;
	--bg-card: rgba(255, 255, 255, 0.7);
	--bg-card-hover: rgba(255, 255, 255, 0.8);
	
	--text-primary: #1e293b;
	--text-secondary: #64748b;
	--text-muted: #94a3b8;
	
	--border-color: rgba(255, 255, 255, 0.3);
	--border-hover: rgba(255, 255, 255, 0.5);
	--sidebar-shadow: 4px 0 15px rgba(0, 0, 0, 0.05);
	--card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.05);
	--card-shadow-hover: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.5);
	
	--accent-primary: #3b82f6;
	--accent-secondary: #6366f1;
	--divider-color: #e2e8f0;

	/* Functional variables used in app */
	--bg-color: var(--bg-primary);
}

:root.dark {
	/* Dark Theme Colors */
	--bg-primary: #0f172a;
	--bg-secondary: #1e293b;
	--bg-sidebar: #1e293b;
	--bg-card: rgba(30, 41, 59, 0.7);
	--bg-card-hover: rgba(30, 41, 59, 0.8);
	
	--text-primary: #f8fafc;
	--text-secondary: #94a3b8;
	--text-muted: #64748b;
	
	--border-color: rgba(255, 255, 255, 0.1);
	--border-hover: rgba(255, 255, 255, 0.2);
	--sidebar-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
	--card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 10px 15px -3px rgba(0, 0, 0, 0.2);
	--card-shadow-hover: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
	
	--divider-color: #334155;
	
	--bg-color: var(--bg-primary);
}

* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;
	transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

body {
	font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
	color: var(--text-primary);
	background-color: var(--bg-color);
	overflow: hidden;
}

/* Layout Structure */
.app-layout {
	display: flex;
	height: 100vh;
	width: 100vw;
}

.main-content {
	flex: 1;
	padding: 2rem;
	overflow-y: auto;
	position: relative;
	background: var(--bg-color);
}

.main-content::before,
.main-content::after {
	content: '';
	position: fixed;
	width: 500px;
	height: 500px;
	border-radius: 50%;
	filter: blur(100px);
	z-index: -1;
	opacity: 0.15;
	pointer-events: none;
}

.main-content::before {
	background: var(--accent-primary);
	top: -100px;
	right: -100px;
}

.main-content::after {
	background: var(--accent-secondary);
	bottom: -100px;
	left: -100px;
}

/* Page Transition Effects */
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

/* Custom Scrollbar for Dark Mode */
.dark ::-webkit-scrollbar {
    width: 10px;
}

.dark ::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

.dark ::-webkit-scrollbar-thumb {
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 2px solid var(--bg-primary);
}

.dark ::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}
</style>