<script setup lang="ts">
import { computed, ref } from 'vue';
import dictpenImg from '../assets/dictpen.png';
import rwkvImg from '../assets/rwkv.png';

// Define types
type Category = 'All' | 'Software' | 'Hardware' | 'Machine Learning';

interface Project {
  id: number;
  title: string;
  category: Exclude<Category, 'All'>;
  description: string;
  link?: string;
  image?: string; // Added image property
  isOngoing?: boolean; // To identify ongoing projects
}

const currentFilter = ref<Category>('All');

const getCategoryIcon = (category: string) => {
  const icons: Record<string, string> = {
    Software: '🖥️',
    Hardware: '⚙️',
    'Machine Learning': '🧠',
  };
  return icons[category] || '🚀';
};

// Separate or Filter specific ongoing projects
const ongoingProjects = ref<Project[]>([
  {
    id: 100,
    title: 'ging-gang: A platform to find real fiends',
    category: 'Software',
    description: 'A platform to find real fiends',
  },
  {
    id: 101,
    title: 'Phone hub: expand your phone',
    category: 'Hardware',
    description:
      'A USB-C hub like device that expand your phone functionality by enabling you plug in any devices you want.',
  },
  {
    id: 102,
    title: 'Fox CAD: A simple CAD built for hobbyist.',
    category: 'Software',
    description: 'Built with Truck(A new CAD kernel in rust)',
  },
]);

const projects: Project[] = [
  {
    id: 1,
    title: 'InferPlaneRCNN',
    category: 'Machine Learning',
    description: 'A better way to infer pre-trained PlaneRCNN model',
    link: 'https://github.com/ovo-Tim/InferPlaneRCNN',
    image:
      'https://github.com/ovo-Tim/InferPlaneRCNN/blob/main/showcase.jpg?raw=true',
  },
  {
    id: 2,
    title: 'EasyProfileFrame',
    category: 'Software',
    description:
      'A FreeCAD workbench designed to simplify the creation of frames using profiles, such as aluminum profiles. It also includes support for exporting Bill of Materials (BOM).',
    link: 'https://github.com/ovo-Tim/EasyProfileFrame',
    image:
      'https://github.com/ovo-Tim/EasyProfileFrame/blob/main/docs/miterCut.png?raw=true',
  },
  {
    id: 3,
    title: 'Crack your Youdao Dictionary Pen S6/S6Pro',
    category: 'Software',
    description: 'Python model using PyTorch to identify bird species.',
    link: 'https://github.com/ovo-Tim/Youdao-DictPenS6P',
    image: dictpenImg,
  },
  {
    id: 4,
    title: 'RWKV-s1',
    category: 'Machine Learning',
    description: 'SFT BlinkDL/rwkv-7-world on simplescaling/s1K-1.1',
    link: 'https://github.com/ovo-Tim/RWKV-s1',
    image: rwkvImg,
  },
  {
    id: 5,
    title: 'mdict2sql',
    category: 'Software',
    description:
      'My first project in Rust. Convert Mdict to SQLite with high speed. Support multithreading.',
    link: 'https://github.com/ovo-Tim/mdict2sql',
  },
];

const filteredProjects = computed(() => {
  if (currentFilter.value === 'All') return projects;
  return projects.filter((p) => p.category === currentFilter.value);
});

const categories: Category[] = [
  'All',
  'Software',
  'Hardware',
  'Machine Learning',
];

const goToProject = (link?: string) => {
  if (link) {
    window.open(link, '_blank', 'noopener,noreferrer');
  }
};
</script>

<template>
    <div class="page-container">

        <!-- ONGOING SECTION (New) -->
        <section class="ongoing-section">
            <div class="invitation-text">
                <h2>🚀 Ongoing Projects</h2>
                <p class="warm-invite">
                    "Building alone is fun, but building together is powerful." <br>
                    We are actively looking for passionate collaborators! Whether you are a designer,
                    coder, or just curious—we'd love to have you on board.
                </p>
            </div>

            <div class="projects-grid">
                <div v-for="project in ongoingProjects" :key="project.id" 
                    class="card ongoing-card" 
                    :class="{ 'clickable': project.link }"
                    @click="goToProject(project.link)">
                    <div class="card-image-wrapper">
                        <img v-if="project.image" :src="project.image" :alt="project.title" loading="lazy" />
                        <div v-else class="card-placeholder" :class="project.category.toLowerCase().replace(' ', '-')">
                            <div class="placeholder-bg"></div>
                            <span class="placeholder-icon">{{ getCategoryIcon(project.category) }}</span>
                        </div>
                        <span class="status-badge">Actively Hiring</span>
                    </div>
                    <div class="card-content">
                        <div class="card-header">
                            <span class="badge" :class="project.category.toLowerCase().replace(' ', '-')">
                                {{ project.category }}
                            </span>
                            <span v-if="project.link" class="link-icon">↗</span>
                        </div>
                        <h3>{{ project.title }}</h3>
                        <p>{{ project.description }}</p>
                    </div>
                </div>
            </div>
        </section>

        <div class="divider"></div>

        <!-- MAIN ARCHIVE SECTION -->
        <section class="archive-section">
            <h1 class="page-title">Project Archive</h1>

            <!-- Filter Buttons -->
            <div class="filters">
                <button v-for="cat in categories" :key="cat" @click="currentFilter = cat"
                    :class="['filter-btn', { active: currentFilter === cat }]">
                    {{ cat }}
                </button>
            </div>

            <!-- Grid -->
            <div class="projects-grid">
                <div v-for="project in filteredProjects" :key="project.id" 
                    class="card project-card"
                    :class="{ 'clickable': project.link }"
                    @click="goToProject(project.link)">
                    <!-- Image on Top -->
                    <div class="card-image-wrapper">
                        <img v-if="project.image" :src="project.image" :alt="project.title" loading="lazy" />
                        <div v-else class="card-placeholder" :class="project.category.toLowerCase().replace(' ', '-')">
                            <div class="placeholder-bg"></div>
                            <span class="placeholder-icon">{{ getCategoryIcon(project.category) }}</span>
                        </div>
                    </div>

                    <!-- Content Below -->
                    <div class="card-content">
                        <div class="card-header">
                            <span class="badge" :class="project.category.toLowerCase().replace(' ', '-')">
                                {{ project.category }}
                            </span>
                            <span v-if="project.link" class="link-icon">↗</span>
                        </div>
                        <h3>{{ project.title }}</h3>
                        <p>{{ project.description }}</p>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 1.5rem;
}

/* --- Ongoing Section Styling --- */
.ongoing-section {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    padding: 4rem 2rem;
    border-radius: 32px;
    margin-bottom: 4rem;
    border: 1px solid var(--border-color);
    box-shadow: var(--card-shadow);
    position: relative;
    overflow: hidden;
}

.ongoing-section::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, var(--accent-primary) 0.1, transparent 70%);
    border-radius: 50%;
    opacity: 0.2;
}

.invitation-text {
    text-align: center;
    max-width: 800px;
    margin: 0 auto 3rem;
}

.invitation-text h2 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1.25rem;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.warm-invite {
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--divider-color), transparent);
    margin: 4rem 0;
}

/* --- Generic Page Styling --- */
.page-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 2.5rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.filters {
    display: flex;
    gap: 1rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.filter-btn {
    border: 1px solid var(--divider-color);
    background: var(--bg-sidebar);
    padding: 0.75rem 1.5rem;
    border-radius: 14px;
    cursor: pointer;
    font-weight: 600;
    color: var(--text-secondary);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-btn:hover {
    background: var(--bg-secondary);
    border-color: var(--text-muted);
    color: var(--text-primary);
}

.filter-btn.active {
    background: var(--text-primary);
    color: var(--bg-primary);
    border-color: var(--text-primary);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}

/* --- Card Grid Styling --- */
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 2.5rem;
}

.card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid var(--border-color);
    box-shadow: var(--card-shadow);
}

.card.clickable {
    cursor: pointer;
}

.card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: var(--card-shadow-hover);
    background: var(--bg-card-hover);
}

/* --- Card Image Area --- */
.card-image-wrapper {
    width: 100%;
    height: 220px;
    position: relative;
    background-color: var(--bg-secondary);
    overflow: hidden;
}

.card-image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover .card-image-wrapper img {
    transform: scale(1.1);
}

.status-badge {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    background: rgba(15, 23, 42, 0.8);
    color: white;
    font-size: 0.75rem;
    padding: 0.5rem 1rem;
    border-radius: 12px;
    font-weight: 700;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* --- Card Content Area --- */
.card-content {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.link-icon {
    font-size: 1.2rem;
    color: var(--text-muted);
    transition: all 0.3s ease;
    opacity: 0.6;
}

.card:hover .link-icon {
    color: var(--accent-primary);
    transform: translate(2px, -2px);
    opacity: 1;
}

.card h3 {
    margin: 1rem 0 0.75rem;
    color: var(--text-primary);
    font-size: 1.4rem;
    font-weight: 800;
    line-height: 1.2;
}

.card p {
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 1rem;
    margin: 0;
}

/* --- Badges --- */
.badge {
    font-size: 0.7rem;
    padding: 0.4rem 1rem;
    border-radius: 10px;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Badge colors */
.badge.software {
    background-color: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
}

.badge.hardware {
    background-color: rgba(235, 68, 68, 0.1);
    color: #eb4444;
}

.badge.machine-learning {
    background-color: rgba(34, 197, 94, 0.1);
    color: #22c55e;
}

/* --- Placeholder Styling --- */
.card-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
}

.card-placeholder.software {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.2) 100%);
    color: #3b82f6;
}

.card-placeholder.hardware {
    background: linear-gradient(135deg, rgba(235, 68, 68, 0.1) 0%, rgba(235, 68, 68, 0.2) 100%);
    color: #f43f5e;
}

.card-placeholder.machine-learning {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.2) 100%);
    color: #10b981;
}

.placeholder-icon {
    font-size: 4.5rem;
    filter: drop-shadow(0 10px 15px rgba(0, 0, 0, 0.1));
    z-index: 1;
    transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card:hover .placeholder-icon {
    transform: scale(1.25) rotate(8deg);
    filter: drop-shadow(0 20px 25px rgba(0, 0, 0, 0.15));
}
</style>