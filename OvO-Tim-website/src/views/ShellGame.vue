<script setup lang="ts">
import { onMounted, ref, nextTick, onBeforeUnmount } from 'vue';
import Matter from 'matter-js';
import bombImg from '../assets/bomb.png';
// Assets
import cupImg from '../assets/cup.png';
import openSourceImg from '../assets/Open_Source_Initiative.svg.png';
import ferrisImg from '../assets/ferris.png';
import kicadImg from '../assets/kicad.png';
import rickrollImg from '../assets/rickroll-roll.gif';

// Game States
type GameState = 'intro' | 'shuffling' | 'hunting' | 'caught' | 'reveal';

const gameState = ref<GameState>('intro');
const message = ref('Welcome! Keep your eyes on the cups.');
const subMessage = ref('');
const gameKey = ref(0);
const cupRefs = ref<HTMLElement[]>([]);
const effectCanvas = ref<HTMLCanvasElement | null>(null);

// Physics Engine Refs
let engine: Matter.Engine | null = null;
let runner: Matter.Runner | null = null;
let shuffleAudio: HTMLAudioElement | null = null;

// Cup Configuration
interface Cup {
  id: number;
  x: number;
  y: number;
  content: 'ferris' | 'bomb' | 'kicad' | 'opensource' | 'rickroll';
  revealed: boolean;
  isFloating: boolean;
  isSlowLift: boolean;
}

const cups = ref<Cup[]>([]);
const descriptions: Record<string, string> = {
  ferris: "I love the design of Rust—it's both elegant and high-performance. It’s a versatile tool that I can use almost anywhere.",
  kicad: 'KiCAD make people bored, cause circuit board is (a) kind of board(bored). :P Besides, it is a really nice EDA tool and I enjoyed a lot when design PCBs with it.',
  opensource: 'Open source gives us a brighter future',
  bomb: 'BOOM!',
  rickroll: "Go to check out Rick Astley's other songs. They are not bad!",
};
const containerWidth = 1000;
const containerHeight = 600;

const cupSpacing = 150;

// Initialize Cups
const initGame = () => {
  // Cleanup Physics first
  cleanupPhysics();
  
  // Clear any existing movement timeouts
  if (moveTimeout) clearTimeout(moveTimeout);
  if (autoMoveTimeout) clearTimeout(autoMoveTimeout);
  moveTimeout = null;
  autoMoveTimeout = null;

  // Reset Game Key to re-render DOM (fixing any exploded elements)
  gameKey.value++;
  cupRefs.value = [];

  // 5 cups centered
  const startX = (containerWidth - 5 * cupSpacing) / 2 + cupSpacing / 2;

  // Shuffle contents assignment
  const contents: Cup['content'][] = [
    'bomb',
    'ferris',
    'kicad',
    'opensource',
    'rickroll',
  ];
  for (let i = contents.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [contents[i], contents[j]] = [contents[j], contents[i]];
  }

  cups.value = Array.from({ length: 5 }, (_, i) => ({
    id: i,
    x: startX + i * cupSpacing,
    y: containerHeight / 2,
    content: contents[i],
    revealed: true,
    isFloating: false,
    isSlowLift: false,
  }));

  message.value = 'Memorize the contents!';
  subMessage.value = 'Click any cup to start shuffling.';
  gameState.value = 'intro';
};

const startGame = async () => {
  // Hide everything
  cups.value.forEach((c) => (c.revealed = false));
  await new Promise((r) => setTimeout(r, 500));

  gameState.value = 'shuffling';
  playShuffleSound();
  message.value = 'Shuffling...';
  subMessage.value = '';

  let shuffles = 20;
  const shuffleInterval = setInterval(() => {
    if (shuffles <= 0) {
      clearInterval(shuffleInterval);
      stopShuffleSound();
      message.value = 'Ready?';
      setTimeout(startFerrisEscape, 2000);
      return;
    }

    const idx1 = Math.floor(Math.random() * cups.value.length);
    let idx2 = Math.floor(Math.random() * cups.value.length);
    while (idx1 === idx2) {
      idx2 = Math.floor(Math.random() * cups.value.length);
    }

    const c1 = cups.value[idx1];
    const c2 = cups.value[idx2];

    // Swap positions (both X and Y)
    const tempX = c1.x;
    const tempY = c1.y;
    
    c1.x = c2.x;
    c1.y = c2.y;
    
    c2.x = tempX;
    c2.y = tempY;

    // Occasionally add vertical chaos to move off the center line
    if (shuffles > 3) {
      const chaosIdx = Math.random() > 0.5 ? idx1 : idx2;
      const verticalRange = containerHeight - 200;
      cups.value[chaosIdx].y = 100 + Math.random() * verticalRange;
    }

    shuffles--;
  }, 500);
};

const startFerrisEscape = () => {
  gameState.value = 'hunting';
  message.value = "Hey! What's that? Catch it!";

  const ferrisCup = cups.value.find((c) => c.content === 'ferris');
  if (ferrisCup) {
    ferrisCup.isFloating = true;
    scheduleAutoMove();
  }
};

// Ferris Run Away Logic
let moveTimeout: ReturnType<typeof setTimeout> | null = null;
let autoMoveTimeout: ReturnType<typeof setTimeout> | null = null;

const moveFerris = () => {
    const ferrisCup = cups.value.find((c) => c.content === 'ferris');
    if (!ferrisCup || gameState.value !== 'hunting') return;

    const margin = 50;
    const newX = margin + Math.random() * (containerWidth - 2 * margin);
    const newY = margin + Math.random() * (containerHeight - 2 * margin);

    ferrisCup.x = newX;
    ferrisCup.y = newY;
}

const onFerrisHover = () => {
  if (gameState.value !== 'hunting') return;
  if (moveTimeout) return;
  moveTimeout = setTimeout(() => {
    moveFerris();
    moveTimeout = null;
  }, 100);
};

const scheduleAutoMove = () => {
  if (gameState.value !== 'hunting') return;
  const delay = 1000 + Math.random() * 2000;
  autoMoveTimeout = setTimeout(() => {
    if (gameState.value === 'hunting') {
      moveFerris();
      scheduleAutoMove();
    }
  }, delay);
};

const catchFerris = () => {
  if (gameState.value !== 'hunting') return;
  if (moveTimeout) { clearTimeout(moveTimeout); moveTimeout = null; }
  if (autoMoveTimeout) { clearTimeout(autoMoveTimeout); autoMoveTimeout = null; }

  gameState.value = 'caught';
  message.value = "I write Rust sometimes, so I guess this makes sense.";
  subMessage.value = "Click other cups to see what's inside.";

  const ferrisCup = cups.value.find((c) => c.content === 'ferris');
  if (ferrisCup) {
    ferrisCup.revealed = true;
    ferrisCup.isFloating = false;
  }
};

const revealCup = (cup: Cup) => {
  if (gameState.value === 'caught' || gameState.value === 'reveal') {
    cup.revealed = true;
    if (cup.content === 'bomb') {
      message.value = 'BOOM!';
      gameState.value = 'reveal';
      
      playExplosionSound();

      // Trigger Explosion
      nextTick(() => {
        const index = cups.value.indexOf(cup);
        // Find the element via ref or fallback to selector
        const el = cupRefs.value[index];
        if (el) {
            const rect = el.getBoundingClientRect();
            const startX = rect.left + rect.width / 2;
            const startY = rect.top + rect.height / 2;
            triggerExplosion(startX, startY);
            createSmoke(startX, startY);
        }
      });
    } else {
        if (cup.content === 'rickroll') {
            playRickrollSound();
        } else if (cup.content === 'opensource') {
            playOpenSourceSound();
            cup.isSlowLift = true;
        }
        gameState.value = 'reveal';
    }
  } else if (gameState.value === 'intro') {
    startGame();
  }
};

const playExplosionSound = () => {
    try {
        const audio = new Audio(new URL('../assets/explosion.mp3', import.meta.url).href);
        audio.volume = 0.6;
        audio.play();
    } catch (e) {
        console.warn("Explosion sound failed", e);
    }
};

const playRickrollSound = () => {
    try {
        const audio = new Audio(new URL('../assets/rickroll.mp3', import.meta.url).href);
        audio.volume = 0.6;
        audio.play();
    } catch (e) {
        console.warn("Rickroll sound failed", e);
    }
};

const playOpenSourceSound = () => {
    try {
        const audio = new Audio(new URL('../assets/arch_intro.mp3', import.meta.url).href);
        audio.volume = 0.6;
        audio.play();
    } catch (e) {
        console.warn("Open Source sound failed", e);
    }
};

const playShuffleSound = () => {
    try {
        if (!shuffleAudio) {
            shuffleAudio = new Audio(new URL('../assets/shuffling.mp3', import.meta.url).href);
            shuffleAudio.loop = true;
            shuffleAudio.volume = 0.4;
        }
        shuffleAudio.play();
    } catch (e) {
        console.warn("Shuffle sound failed", e);
    }
};

const stopShuffleSound = () => {
    if (shuffleAudio) {
        shuffleAudio.pause();
        shuffleAudio.currentTime = 0;
    }
};

// Smoke Effect Logic
interface Particle {
    x: number;
    y: number;
    vx: number;
    vy: number;
    life: number;
    maxLife: number;
    size: number;
    rotation: number;
    color: string;
}

let particles: Particle[] = [];
let animationFrameId: number | null = null;

const createSmoke = (x: number, y: number) => {
    if (!effectCanvas.value) return;
    const ctx = effectCanvas.value.getContext('2d');
    if (!ctx) return;
    
    // Set canvas size to full screen if not set
    effectCanvas.value.width = window.innerWidth;
    effectCanvas.value.height = window.innerHeight;

    // Create particles
    for (let i = 0; i < 50; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 2 + 1; // Slower initial speed
        particles.push({
            x: x,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            life: 1.0,
            maxLife: 1.0,
            size: Math.random() * 15 + 5,
            rotation: Math.random() * Math.PI * 2,
            color: `rgba(${120 + Math.random()*40}, ${120 + Math.random()*40}, ${120 + Math.random()*40},` // Brighter grey
        });
    }
    
    if (!animationFrameId) {
        updateParticles();
    }
};

const updateParticles = () => {
    if (!effectCanvas.value) return;
    const ctx = effectCanvas.value.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, effectCanvas.value.width, effectCanvas.value.height);

    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vx *= 0.98; // Less drag for smoother/slower movement
        p.vy *= 0.98;
        p.size += 0.2; // Slower expansion
        p.life -= 0.008; // Slower fade (lasts longer)

        if (p.life <= 0) {
            particles.splice(i, 1);
        } else {
            ctx.save();
            ctx.translate(p.x, p.y);
            // ctx.rotate(p.rotation); // Rotating circles doesn't show much, skipping for perf
            ctx.beginPath();
            ctx.arc(0, 0, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `${p.color} ${p.life * 0.5})`; // Max opacity 0.5
            ctx.fill();
            ctx.restore();
        }
    }

    if (particles.length > 0) {
        animationFrameId = requestAnimationFrame(updateParticles);
    } else {
        animationFrameId = null;
        ctx.clearRect(0, 0, effectCanvas.value.width, effectCanvas.value.height);
    }
};

// Physics Logic
const triggerExplosion = (originX: number, originY: number) => {
    const Engine = Matter.Engine,
        Runner = Matter.Runner,
        Bodies = Matter.Bodies,
        Composite = Matter.Composite,
        Mouse = Matter.Mouse,
        MouseConstraint = Matter.MouseConstraint;

    engine = Engine.create();
    engine.timing.timeScale = 0.5; // Half speed simulation
    const world = engine.world;

    // Elements to explode: Title, Message, Cups
    const elements = [
        document.querySelector('.game-title'),
        document.querySelector('.message-board'),
        ...document.querySelectorAll('.cup-wrapper')
    ].filter(el => el) as HTMLElement[];

    // Ground/Walls
    const width = window.innerWidth;
    const height = window.innerHeight;
    const ground = Bodies.rectangle(width / 2, height + 200, width, 100, { isStatic: true });
    Composite.add(world, [ground]);

    const bodies: Matter.Body[] = [];

    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        el.style.width = `${rect.width}px`;
        el.style.height = `${rect.height}px`;
        
        // Center
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;

        const body = Bodies.rectangle(x, y, rect.width, rect.height, {
            restitution: 0.6,
            friction: 0.1,
            density: 0.002
        });
        
        body.render.element = el;
        bodies.push(body);
        
        // Detach
        el.style.position = 'fixed';
        el.style.top = '0';
        el.style.left = '0';
        el.style.margin = '0';
        el.style.transform = `translate(${x}px, ${y}px)`; 
        el.style.zIndex = '1000';
    });

    Composite.add(world, bodies);

    // Add Explosion Force
    bodies.forEach(body => {
        const forceMagnitude = 0.15 * body.mass; // Reduced force
        const dx = body.position.x - originX;
        const dy = body.position.y - originY;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;

        Matter.Body.applyForce(body, body.position, {
            x: (dx / dist) * forceMagnitude,
            y: (dy / dist) * forceMagnitude - 0.03 * body.mass // Less lift
        });
        
        Matter.Body.setAngularVelocity(body, (Math.random() - 0.5) * 0.2); // Slower spinning
    });

    const mouse = Mouse.create(document.body);
    const mouseConstraint = MouseConstraint.create(engine, {
        mouse: mouse,
        constraint: { stiffness: 0.2, render: { visible: false } }
    });
    Composite.add(world, mouseConstraint);

    Matter.Events.on(engine, 'afterUpdate', () => {
        bodies.forEach(body => {
            const el = body.render.element as HTMLElement;
            if (el) {
                const { x, y } = body.position;
                el.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) rotate(${body.angle}rad)`;
            }
        });
    });

    runner = Runner.create();
    Runner.run(runner, engine);
};

const cleanupPhysics = () => {
    if (runner) Matter.Runner.stop(runner);
    if (engine) Matter.Engine.clear(engine);
    runner = null;
    engine = null;
    
    // Also clear particles and sound
    particles = [];
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    stopShuffleSound();
    /* Clear canvas: handled in update loop when particles empty or next frame */
};

onMounted(() => {
  initGame();
});

onBeforeUnmount(() => {
    cleanupPhysics();
});
</script>

<template>
    <div class="shell-game-container">
        <!-- Canvas for effects -->
        <canvas ref="effectCanvas" class="effect-canvas"></canvas>

        <!-- Wraps game elements for easy DOM reset -->
        <div class="game-scene" :key="gameKey">
            <h2 class="game-title">Know Me More</h2>
            <div class="message-board">
                <p>{{ message }}</p>
                <small>{{ subMessage }}</small>
            </div>

            <div class="game-area" :style="{ width: containerWidth + 'px', height: containerHeight + 'px' }">
                <div 
                    v-for="(cup, index) in cups" 
                    :key="cup.id"
                    :ref="(el) => { if(el) cupRefs[index] = el as HTMLElement }"
                    class="cup-wrapper"
                    :class="{ 'floating': cup.isFloating, 'caught': gameState === 'caught' && cup.content === 'ferris' }"
                    :style="{ transform: `translate(${cup.x - 50}px, ${cup.y - 50}px)` }"
                    @click="revealCup(cup)"
                >
                    <!-- The Content (Hidden or Shown) -->
                    <div class="content" :class="{ 'visible': cup.revealed || (cup.isFloating && cup.content === 'ferris') }">
                        <div class="icon-with-text">
                            <div v-if="cup.content === 'opensource'" class="sunshine-effect" :class="{ 'active': cup.isSlowLift }"></div>
                            <template v-if="cup.content === 'ferris'">
                                <img :src="ferrisImg" class="item-icon ferris" :class="{ 'blurry': gameState === 'intro' }" alt="Ferris" />
                            </template>
                            <template v-else-if="cup.content === 'bomb'">
                                <img :src="bombImg" class="item-icon bomb" alt="Bomb" />
                            </template>
                            <template v-else-if="cup.content === 'kicad'">
                                <img :src="kicadImg" class="item-icon" :class="{ 'blurry': gameState === 'intro' }" alt="KiCAD" />
                            </template>
                            <template v-else-if="cup.content === 'opensource'">
                                <img :src="openSourceImg" class="item-icon" :class="{ 'blurry': gameState === 'intro' }" alt="Open Source" />
                            </template>
                            <template v-else-if="cup.content === 'rickroll'">
                                <img :src="rickrollImg" class="item-icon rickroll" :class="{ 'blurry': gameState === 'intro' }" alt="Rickroll" />
                            </template>
                            <span v-else class="item-icon placeholder" :class="{ 'blurry': gameState === 'intro' }">?</span>

                            <p v-if="gameState !== 'intro' && cup.revealed && descriptions[cup.content]" class="item-description">
                                {{ descriptions[cup.content] }}
                            </p>
                            <p v-if="cup.content === 'bomb' && gameState === 'intro'" class="bomb-warning">
                                Oh my, you'd better keep an eye on this
                            </p>
                        </div>
                    </div>

                    <!-- The Cup -->
                    <div 
                        class="cup" 
                        :class="{ 'lifted': cup.revealed || cup.isFloating, 'slow-lift': cup.isSlowLift }"
                        @mouseover="cup.content === 'ferris' ? onFerrisHover() : null"
                        @mousedown.stop="cup.content === 'ferris' && gameState === 'hunting' ? catchFerris() : null"
                        @click.stop="cup.content === 'ferris' && gameState === 'hunting' ? null : revealCup(cup)"
                    >
                        <img :src="cupImg" alt="Cup" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Effect Canvas */
.effect-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 9999; /* On top of everything */
}

.shell-game-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--text-primary);
    overflow: hidden;
    position: relative;
    width: 100%;
}

.game-scene {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.game-title {
    margin-bottom: 1rem;
    font-size: 2rem;
    font-weight: 700;
}

.message-board {
    margin-bottom: 2rem;
    text-align: center;
    height: 60px;
}

.game-area {
    position: relative;
    border: 2px dashed var(--border-color);
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.05);
}

.cup-wrapper {
    position: absolute;
    width: 100px;
    height: 120px;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    transition: transform 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
    cursor: pointer;
}

.content {
    position: absolute;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
    z-index: 1;
    width: max-content;
}

.content.visible {
    opacity: 1;
}

.icon-with-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    position: relative;
}

.item-description {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.75rem;
    color: var(--text-secondary);
    line-height: 1.4;
    text-align: center;
    margin-top: 10px;
    background: rgba(15, 15, 20, 0.85);
    padding: 8px 12px;
    border-radius: 12px;
    white-space: normal;
    width: 200px;
    animation: fadeIn 0.3s ease;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

.bomb-warning {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.85rem;
    color: #ff4d4d;
    font-weight: 800;
    text-align: center;
    margin-top: 15px;
    background: rgba(255, 0, 0, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 77, 77, 0.3);
    padding: 8px 16px;
    border-radius: 20px;
    white-space: normal;
    width: 160px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
    animation: pulse-danger 2s infinite ease-in-out;
}

@keyframes pulse-danger {
    0%, 100% {
        transform: scale(1);
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
    }
    50% {
        transform: scale(1.05);
        box-shadow: 0 4px 25px rgba(255, 0, 0, 0.4);
        border-color: rgba(255, 77, 77, 0.6);
    }
}

.item-icon {
    width: 80px;
    height: auto;
    max-height: 80px;
    object-fit: contain;
}

.item-icon.bomb {
     width: 60px;
     height: 60px;
     filter: drop-shadow(0 0 5px red);
}

.item-icon.rickroll {
    width: 100px;
    height: 100px;
}

.cup {
    position: absolute;
    bottom: 0;
    width: 100px;
    height: 100px;
    transition: transform 0.3s ease;
    z-index: 2;
}

.cup img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transform: rotate(180deg);
}

.item-icon.blurry {
    filter: blur(10px);
}

.cup.lifted {
    transform: translateY(-100px);
}

.cup.slow-lift {
    transition: transform 10s cubic-bezier(0.4, 0, 0.2, 1) !important;
    transform: translateY(-220px) !important;
}

.sunshine-effect {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    background: repeating-conic-gradient(
        from 0deg,
        rgba(255, 255, 200, 0.4) 0deg 10deg,
        transparent 10deg 20deg
    );
    border-radius: 50%;
    -webkit-mask-image: radial-gradient(circle, black 30%, transparent 70%);
    mask-image: radial-gradient(circle, black 30%, transparent 70%);
    z-index: -1;
    pointer-events: none;
    opacity: 0;
    transition: opacity 2s ease;
}

.sunshine-effect.active {
    opacity: 1;
    animation: rotate-sunshine 15s linear infinite;
}

@keyframes rotate-sunshine {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
}

.cup-wrapper.floating .cup {
     transform: translateX(3px) translateY(-50px) rotate(10deg);
}

.cup-wrapper.floating {
    z-index: 100;
    transition: transform 0.8s ease-out;
}

.restart-btn {
    position: fixed;
    bottom: 10vh;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 30px;
    background: var(--accent-primary);
    color: white;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    font-weight: 800;
    font-size: 1.2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    z-index: 2000;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.restart-btn:hover {
    transform: translateX(-50%) scale(1.1);
    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
