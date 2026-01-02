<template>
    <div class="page-container">
        <h1 class="page-title">Personal Info</h1>

        <div class="card intro-card">
            <h2>Hi there! 👋</h2>
            <p>
                I enjoy mechanics and love building cool projects.
                <br />
                I code mostly in Python and Rust🦀, and sometimes I
                build GUI application with Vue3 and <a href="https://tauri.app/" target="_blank">Tauri</a>.
                Also diving into machine learning and deep learning these days.
                <br />
                <br />
                One the hardware side, I'm learning to design PCBs with KiCad and got some experience in modeling with
                FreeCAD
                and Shaper3D, bring them to the reality through 3D printing. (But I'm somehow not satisfied with any of
                these
                tools, so I'm planning to build one
                myself. Check the project section for more details.)
                <br />
                <br />
                Looking for new friends who vibe with the same interests! Slide into my DMs on Discord or email me –
                let’s hang out! 🎉
            </p>
        </div>

        <div class="stats-grid">
            <div class="card stat-card">
                <h3>Location</h3>
                <p class="card-text">Shanghai, China</p>
            </div>
            <div class="card stat-card">
                <h3>System</h3>
                <p class="card-text">Arch Linux (laptop)</p>
                <p class="card-text">Debian/Armbian (server)</p>
            </div>
        </div>

        <div class="boost-container">
            <p v-if="physicsEnabled" class="leak-msg">Oh no! The WD40 leaked.</p>
            <button class="btn-modern" @click="startPhysics">Boost the server by WD40</button>
        </div>
    </div>
</template>

<style scoped>
.page-container {
    max-width: 1000px;
    margin: 0 auto;
}

.page-title {
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #2c3e50;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    /* The 3D Floating Shadow */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    margin-bottom: 2rem;
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-5px);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
}

.stat-card h3 {
    color: #888;
    font-size: 0.9rem;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.stat-card p {
    font-size: 1.3rem;
    font-weight: bold;
    color: #333;
    text-align: center;
}

.btn-modern {
    /* Layout & Sizing */
    display: inline-block;
    padding: 12px 28px;
    font-family: 'Inter', sans-serif;
    /* Or any clean sans-serif */
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    border: none;
    border-radius: 8px;
    /* Rounded corners for a modern feel */

    /* Colors & Styling */
    color: #ffffff;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

    /* Smooth Animation */
    transition: all 0.2s ease-in-out;
}

/* Hover State */
.btn-modern:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    transform: translateY(-1px);
    /* Lifts the button slightly */
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Click/Active State */
.btn-modern:active {
    transform: translateY(0);
    filter: brightness(0.9);
}

/* Focus State (Accessibility) */
.btn-modern:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

.boost-container {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
    z-index: 2000;
}

.leak-msg {
    background: #fee2e2;
    color: #ef4444;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>

<script setup>
import { ref, onBeforeUnmount } from 'vue';
import Matter from 'matter-js';

// Refs
const physicsEnabled = ref(false);
let engine = null;
let render = null;
let runner = null;

const startPhysics = () => {
    if (physicsEnabled.value) return; // Prevent double clicking
    physicsEnabled.value = true;

    // 1. Setup Matter.js Engine
    const Engine = Matter.Engine,
        Render = Matter.Render, // We won't use the canvas render, but we need the engine
        Runner = Matter.Runner,
        Bodies = Matter.Bodies,
        Composite = Matter.Composite,
        Mouse = Matter.Mouse,
        MouseConstraint = Matter.MouseConstraint;

    engine = Engine.create();
    const world = engine.world;

    // 2. Select elements to physics-ify
    // We select cards, the title, and even the button itself
    const elements = document.querySelectorAll('.card, .page-title');
    const bodies = [];

    // 3. Create the Ground and Walls (so things don't fall forever)
    const width = window.innerWidth;
    const height = window.innerHeight; // Or document.body.scrollHeight for full page

    const ground = Bodies.rectangle(width / 2, height + 50, width, 100, { isStatic: true });
    const leftWall = Bodies.rectangle(-50, height / 2, 100, height * 2, { isStatic: true });
    const rightWall = Bodies.rectangle(width + 50, height / 2, 100, height * 2, { isStatic: true });

    Composite.add(world, [ground, leftWall, rightWall]);

    // 4. Convert DOM elements to Physics Bodies
    elements.forEach((el) => {
        const rect = el.getBoundingClientRect();

        el.style.userSelect = 'none';

        // Save current computed width/height so they don't shrink when Position becomes Absolute
        el.style.width = `${rect.width}px`;
        el.style.height = `${rect.height}px`;

        // Calculate center of the element (Matter.js uses center, DOM uses top-left)
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;

        // Create a rigid body
        const body = Bodies.rectangle(x, y, rect.width, rect.height, {
            restitution: 0.5, // Bounciness (0-1)
            friction: 0.1,
            density: 0.001
        });

        // Store reference to DOM element inside the body
        body.render.element = el;
        bodies.push(body);
    });

    // 5. "Detach" elements from DOM layout and set to absolute
    // We do this AFTER getting coordinates to avoid layout shifts before calculations
    elements.forEach((el) => {
        el.style.position = 'fixed'; // Fixed so they fall relative to the viewport
        el.style.top = '0';
        el.style.left = '0';
        el.style.margin = '0';
        el.style.transformOrigin = 'center center';
        el.style.zIndex = '1000';
    });

    Composite.add(world, bodies);

    // 6. Add Mouse Interaction (So you can drag the elements!)
    const mouse = Mouse.create(document.body);
    const mouseConstraint = MouseConstraint.create(engine, {
        mouse: mouse,
        constraint: {
            stiffness: 0.2,
            render: { visible: false }
        }
    });
    Composite.add(world, mouseConstraint);

    // 7. Custom Render Loop (Sync Physics -> CSS)
    const updateLoop = () => {
        if (!engine) return;

        // Update physics
        Matter.Engine.update(engine, 1000 / 60);

        // Sync CSS transforms
        bodies.forEach((body) => {
            const el = body.render.element;
            if (el) {
                const { x, y } = body.position;
                const angle = body.angle;
                // Translate moves center to 0,0, so we simply move to x,y
                // But since fixed top/left is 0, we translate exactly to body position minus half width/height?
                // Actually easier: translate to body.x and body.y, but offset by percent to center it
                el.style.transform = `translate(${x - body.bounds.max.x + body.bounds.min.x + (body.bounds.max.x - body.bounds.min.x) / 2}px, ${y}px) translate(-50%, -50%) rotate(${angle}rad)`;

                // Simplified math for translate:
                // DOM (0,0) is top-left. Body (x,y) is center.
                // We set top:0 left:0.
                // We want to move element center to x,y.
                el.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) rotate(${angle}rad)`;
            }
        });

        requestAnimationFrame(updateLoop);
    };

    updateLoop();
};

// Cleanup just in case
onBeforeUnmount(() => {
    if (engine) {
        Matter.Engine.clear(engine);
        engine = null;
    }
});
</script>
