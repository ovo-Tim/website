<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'

const isCollapsed = ref(false)

// Function to check window width and adjust state
const checkScreenSize = () => {
	// Collapse sidebar if screen is narrower than 1024px
	isCollapsed.value = window.innerWidth < 1024
}

// Set up listeners when the app loads
onMounted(() => {
	checkScreenSize()
	window.addEventListener('resize', checkScreenSize)
})

// Clean up listeners when the app closes
onUnmounted(() => {
	window.removeEventListener('resize', checkScreenSize)
})
</script>

<template>
	<div class="app-layout">
		<!-- Navigation Left -->
		<Sidebar :isCollapsed="isCollapsed" />

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
/* Global Resets */
:root {
	--bg-color: #f4f7f6;
	/* Light grey background makes white cards pop */
	--text-primary: #2c3e50;
}

* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;
}

body {
	font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
	color: var(--text-primary);
	background-color: var(--bg-color);
	overflow: hidden;
	/* Prevent body scroll, let main-content scroll */
}

/* Layout Structure */
.app-layout {
	display: flex;
	height: 100vh;
	width: 100vw;
}

.main-content {
	flex: 1;
	/* Takes up remaining space */
	padding: 2rem;
	overflow-y: auto;
	/* Adds scrollbar only to content area */
	position: relative;
}

/* Page Transition Effects (Optional but nice) */
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>