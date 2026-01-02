<script setup lang="ts">
import { ref, computed } from 'vue'

// Define types
type Category = 'All' | 'Software' | 'Hardware' | 'Machine Learning'

interface Project {
    id: number
    title: string
    category: Exclude<Category, 'All'>
    description: string
    link?: string
    image?: string // Added image property
    isOngoing?: boolean, // To identify ongoing projects
}

const currentFilter = ref<Category>('All')

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
        description: 'A USB-C hub like device that expand your phone functionality by enabling you plug in any devices you want.',
    },
])

const projects: Project[] = [
    {
        id: 1,
        title: 'InferPlaneRCNN',
        category: 'Machine Learning',
        description: 'A better way to infer pre-trained PlaneRCNN model',
        link: 'https://github.com/ovo-Tim/InferPlaneRCNN',
        image: 'https://github.com/ovo-Tim/InferPlaneRCNN/blob/main/showcase.jpg?raw=true'
    },
    {
        id: 2,
        title: 'EasyProfileFrame',
        category: 'Software',
        description: 'A FreeCAD workbench designed to simplify the creation of frames using profiles, such as aluminum profiles. It also includes support for exporting Bill of Materials (BOM).',
        link: 'https://github.com/ovo-Tim/EasyProfileFrame',
        image: 'https://github.com/ovo-Tim/EasyProfileFrame/blob/main/docs/miterCut.png?raw=true'
    },
    {
        id: 3,
        title: 'Crack your Youdao Dictionary Pen S6/S6Pro',
        category: 'Software',
        description: 'Python model using PyTorch to identify bird species.',
        link: 'https://github.com/ovo-Tim/Youdao-DictPenS6P',
        image: '../assets/dictpen.png'
    },
    {
        id: 4,
        title: 'RWKV-s1',
        category: 'Machine Learning',
        description: 'SFT BlinkDL/rwkv-7-world on simplescaling/s1K-1.1',
        link: 'https://github.com/ovo-Tim/RWKV-s1',
        image: '../assets/rwkv.png'
    },
    {
        id: 5,
        title: 'mdict2sql',
        category: 'Software',
        description: 'Convert Mdict to SQLite in a high speed. Support multithreading now.',
        link: 'https://github.com/ovo-Tim/mdict2sql',
    }
]

const filteredProjects = computed(() => {
    if (currentFilter.value === 'All') return projects
    return projects.filter(p => p.category === currentFilter.value)
})

const categories: Category[] = ['All', 'Software', 'Hardware', 'Machine Learning']
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
                <button class="join-btn">Message me to Join!</button>
            </div>

            <div class="projects-grid">
                <div v-for="project in ongoingProjects" :key="project.id" class="card ongoing-card">
                    <div class="card-image-wrapper">
                        <img :src="project.image" :alt="project.title" loading="lazy" />
                        <span class="status-badge">Actively Hiring</span>
                    </div>
                    <div class="card-content">
                        <span class="badge" :class="project.category.toLowerCase().replace(' ', '-')">
                            {{ project.category }}
                        </span>
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
                <div v-for="project in filteredProjects" :key="project.id" class="card project-card">
                    <!-- Image on Top -->
                    <div class="card-image-wrapper">
                        <img :src="project.image" :alt="project.title" loading="lazy" />
                    </div>

                    <!-- Content Below -->
                    <div class="card-content">
                        <span class="badge" :class="project.category.toLowerCase().replace(' ', '-')">
                            {{ project.category }}
                        </span>
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
    max-width: 1100px;
    margin: 0 auto;
    padding: 2rem 1rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- Ongoing Section Styling --- */
.ongoing-section {
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    padding: 2.5rem;
    border-radius: 24px;
    margin-bottom: 3rem;
    border: 1px solid #e1e4e8;
}

.invitation-text {
    text-align: center;
    max-width: 600px;
    margin: 0 auto 2.5rem;
}

.invitation-text h2 {
    font-size: 2.2rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.warm-invite {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #555;
    margin-bottom: 1.5rem;
}

.join-btn {
    background: #2c3e50;
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, background 0.2s;
}

.join-btn:hover {
    background: #3e5871;
    transform: scale(1.05);
}

.divider {
    height: 1px;
    background: #eee;
    margin: 3rem 0;
}

/* --- Generic Page Styling --- */
.page-title {
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.filters {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.filter-btn {
    border: none;
    background: transparent;
    padding: 0.6rem 1.4rem;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    color: #7f8c8d;
    transition: all 0.2s;
    background: #f8f9fa;
}

.filter-btn:hover {
    background: #e9ecef;
}

.filter-btn.active {
    background: #2c3e50;
    color: white;
    box-shadow: 0 4px 10px rgba(44, 62, 80, 0.2);
}

/* --- Card Grid Styling --- */
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}

.card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    /* Ensures image corners follow border radius */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #f0f0f0;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.ongoing-card {
    border: 2px solid #2c3e50;
    /* Highlight ongoing projects */
}

/* --- Card Image Area --- */
.card-image-wrapper {
    width: 100%;
    height: 180px;
    position: relative;
    background-color: #eee;
}

.card-image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.status-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(44, 62, 80, 0.9);
    color: white;
    font-size: 0.7rem;
    padding: 4px 10px;
    border-radius: 12px;
    font-weight: bold;
    backdrop-filter: blur(4px);
}

/* --- Card Content Area --- */
.card-content {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.card h3 {
    margin: 0.8rem 0 0.5rem;
    color: #2c3e50;
    font-size: 1.25rem;
}

.card p {
    color: #666;
    line-height: 1.5;
    font-size: 0.95rem;
    margin: 0;
}

/* --- Badges --- */
.badge {
    font-size: 0.75rem;
    padding: 0.3rem 0.8rem;
    border-radius: 50px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Badge colors */
.badge.software {
    background-color: #e3f2fd;
    color: #1976d2;
}

.badge.hardware {
    background-color: #fbe9e7;
    color: #d84315;
}

.badge.machine-learning {
    background-color: #e8f5e9;
    color: #2e7d32;
}
</style>