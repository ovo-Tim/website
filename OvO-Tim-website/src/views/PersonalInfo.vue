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
            <div class="tooltip">Boost the server with WD40</div>
            <button class="btn-wd40" @click="startPhysics">
                <img src="../assets/WD-40_logo.svg" alt="WD40" class="wd40-icon" />
            </button>
        </div>
    </div>
</template>

<style scoped>
.page-container {
    max-width: 1000px;
    margin: 0 auto;
}

.page-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 2.5rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 24px;
    padding: 2.5rem;
    border: 1px solid var(--border-color);
    box-shadow: var(--card-shadow);
    margin-bottom: 2rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    will-change: transform;
}

.card.is-falling {
    transition: none !important;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.1),
        transparent
    );
    transition: 0.5s;
}

.card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: var(--card-shadow-hover);
    border: 1px solid var(--border-hover);
    background: var(--bg-card-hover);
}

.card:hover::before {
    left: 100%;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
}

.stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem;
}

.stat-card h3 {
    color: var(--text-secondary);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
    font-weight: 700;
}

.stat-card p {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0.25rem 0;
}

.btn-modern {
    display: inline-block;
    padding: 12px 28px;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    border: none;
    border-radius: 8px;
    color: #ffffff;
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: all 0.2s ease-in-out;
}

.btn-modern:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.btn-modern:active {
    transform: translateY(0);
    filter: brightness(0.9);
}

.btn-modern:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

.btn-wd40 {
    background: var(--bg-sidebar);
    border: none;
    border-radius: 50%;
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    padding: 12px;
}

.btn-wd40:hover {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.btn-wd40:active {
    transform: scale(0.95);
}

.btn-wd40:hover + .tooltip,
.btn-wd40:hover ~ .tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

.wd40-icon {
    width: 100%;
    height: auto;
    object-fit: contain;
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

.tooltip {
    position: absolute;
    bottom: calc(100% + 10px);
    right: 0;
    background: var(--bg-secondary);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s ease;
    transform: translateY(5px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border: 1px solid var(--border-color);
}

.tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    right: 25px;
    border-width: 5px;
    border-style: solid;
    border-color: var(--bg-secondary) transparent transparent transparent;
}

.boost-container:hover .tooltip {
    opacity: 1;
    transform: translateY(0);
}

.leak-msg {
    background: #fee2e2;
    color: #ef4444;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    animation: fadeIn 0.3s ease;
}

.dark .leak-msg {
    background: #450a0a;
    color: #fca5a5;
    border-color: rgba(252, 165, 165, 0.2);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
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
        el.classList.add('is-falling');
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
            stiffness: 0.3, // Snappier dragging
            render: { visible: false }
        }
    });
    Composite.add(world, mouseConstraint);

    // 7. Sync Physics to CSS
    Matter.Events.on(engine, 'afterUpdate', () => {
        bodies.forEach((body) => {
            const el = body.render.element;
            if (el) {
                const { x, y } = body.position;
                el.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) rotate(${body.angle}rad)`;
            }
        });
    });

    // 8. Run the Engine
    runner = Runner.create();
    Runner.run(runner, engine);
};

// Cleanup
onBeforeUnmount(() => {
    if (runner) Matter.Runner.stop(runner);
    if (engine) Matter.Engine.clear(engine);
    engine = null;
    runner = null;
});
</script>
