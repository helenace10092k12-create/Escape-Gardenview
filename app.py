import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Escape Gardenview - FNAF 8-bit Minigame",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit UI Chrome
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0; margin: 0; max-width: 100vw;}
        iframe {display: block; border: none;}
    </style>
""", unsafe_allow_html=True)

# HTML5/JS FNAF Pixel Minigame Engine
game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gardenview 8-Bit Death Minigame</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        * {
            box-sizing: border-box;
            user-select: none;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #000;
            color: #fff;
            font-family: 'Press Start 2P', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        #game-wrapper {
            position: relative;
            width: 800px;
            height: 600px;
            background: #000;
            border: 4px solid #1a1a1a;
            box-shadow: 0 0 40px rgba(160, 32, 240, 0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Top Bar */
        #top-bar {
            height: 48px;
            background: #080808;
            border-bottom: 3px solid #222;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 16px;
            z-index: 10;
        }

        .title-text {
            color: #d32f2f;
            font-size: 11px;
            letter-spacing: 1px;
            text-shadow: 2px 2px #000;
        }

        .lang-btn {
            background: #111;
            color: #ffb74d;
            border: 2px solid #ffb74d;
            padding: 6px 10px;
            font-size: 9px;
            cursor: pointer;
            font-family: 'Press Start 2P', monospace;
        }

        .lang-btn:hover {
            background: #ffb74d;
            color: #000;
        }

        /* Canvas Screen */
        #canvas-container {
            position: relative;
            width: 800px;
            height: 440px;
            background: #000;
        }

        canvas {
            display: block;
            width: 100%;
            height: 100%;
            image-rendering: pixelated;
        }

        /* CRT Scanlines and Static Effects */
        #crt-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
            background-size: 100% 4px, 6px 100%;
            z-index: 4;
        }

        #static-canvas {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            opacity: 0.08;
            z-index: 3;
        }

        /* FNAF Typewriter Banner */
        #fnaf-banner {
            position: absolute;
            top: 15px;
            width: 100%;
            text-align: center;
            font-size: 16px;
            color: #ff0055;
            text-shadow: 3px 3px #000;
            z-index: 5;
            letter-spacing: 4px;
        }

        /* Bottom Dialogue/UI Box */
        #bottom-ui {
            height: 112px;
            background: #050505;
            border-top: 3px solid #333;
            padding: 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }

        #dialogue-text {
            color: #fff;
            font-size: 10px;
            line-height: 1.6;
            min-height: 40px;
        }

        #controls-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px dashed #333;
            padding-top: 8px;
        }

        .party-selector {
            display: flex;
            gap: 12px;
        }

        .char-btn {
            background: #111;
            border: 2px solid #444;
            color: #888;
            font-size: 8px;
            padding: 5px 8px;
            cursor: pointer;
            font-family: 'Press Start 2P', monospace;
        }

        .char-btn.active {
            border-color: #ab47bc;
            color: #ab47bc;
            background: #1a0926;
            box-shadow: 0 0 10px #ab47bc;
        }

        #item-status {
            font-size: 9px;
            color: #ffeb3b;
        }

        /* Virtual D-Pad for Mobile/Touch */
        #touch-controls {
            display: none;
            position: absolute;
            bottom: 120px;
            right: 15px;
            z-index: 6;
            grid-template-columns: repeat(3, 40px);
            grid-template-rows: repeat(3, 40px);
            gap: 5px;
        }

        .d-btn {
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid #fff;
            color: #fff;
            font-size: 14px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 4px;
        }

        @media (max-width: 820px) {
            #game-wrapper { width: 100vw; height: 100vh; border: none; }
            #canvas-container { width: 100vw; height: calc(100vh - 160px); }
            #touch-controls { display: grid; }
        }
    </style>
</head>
<body>

<div id="game-wrapper">
    <!-- Top Bar -->
    <div id="top-bar">
        <div class="title-text" id="title-text">GARDENVIEW - MINIGAME</div>
        <button class="lang-btn" id="lang-btn" onclick="toggleLanguage()">VIE / ENG</button>
    </div>

    <!-- Main Game Canvas -->
    <div id="canvas-container">
        <canvas id="gameCanvas" width="800" height="440"></canvas>
        <canvas id="static-canvas" width="400" height="220"></canvas>
        <div id="crt-overlay"></div>
        <div id="fnaf-banner">S A V E . T H E M</div>

        <!-- Touch Controls -->
        <div id="touch-controls">
            <div></div><div class="d-btn" id="btn-up">▲</div><div></div>
            <div class="d-btn" id="btn-left">◄</div><div class="d-btn" id="btn-action">E</div><div class="d-btn" id="btn-right">►</div>
            <div></div><div class="d-btn" id="btn-down">▼</div><div></div>
        </div>
    </div>

    <!-- Bottom Dialogue UI -->
    <div id="bottom-ui">
        <div id="dialogue-text">WASD / Arrow Keys to move. [1][2][3] to switch character. Collect Ichor and Keycards!</div>
        <div id="controls-bar">
            <div class="party-selector">
                <button class="char-btn active" id="btn-yatta" onclick="switchChar('yatta')">[1] YATTA</button>
                <button class="char-btn" id="btn-looey" onclick="switchChar('looey')">[2] LOOEY</button>
                <button class="char-btn" id="btn-blot" onclick="switchChar('blot')">[3] BLOT</button>
            </div>
            <div id="item-status">ICHOR: <span id="ichor-count">0</span>/3 | KEYCARD: <span id="key-status">NO</span></div>
        </div>
    </div>
</div>

<script>
// --- AUDIO SYNTHESIZER (8-BIT WEBAUDIO) ---
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
}

function playSynthTone(freq, duration, type='square') {
    if (!audioCtx) return;
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch(e){}
}

function playStepSound() {
    playSynthTone(120 + Math.random()*40, 0.05, 'triangle');
}

function playPickupSound() {
    playSynthTone(440, 0.08, 'square');
    setTimeout(() => playSynthTone(880, 0.12, 'square'), 80);
}

function playGlitchJumpscareSound() {
    if (!audioCtx) return;
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(80, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(400, audioCtx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
    } catch(e){}
}

// --- GAME STATE ---
let currentLang = 'ENG';
let activeChar = 'yatta'; // 'yatta', 'looey', 'blot'
let ichorCollected = 0;
let hasKeycard = false;
let bannerTimer = 0;
let bannerText = "S A V E . T H E M";

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const staticCanvas = document.getElementById("static-canvas");
const staticCtx = staticCanvas.getContext("2d");

// Language Dictionary
const strings = {
    ENG: {
        title: "GARDENVIEW - MINIGAME",
        banners: ["S A V E . T H E M", "H E L P . U S", "F O L L O W . M E", "R U N . A W A Y"],
        dialogue_start: "WASD/Arrows to move. [1][2][3] to switch character. Find 3 Ichor Canisters & Elevator Keycard!",
        dialogue_yatta: "Yatta selected! [Passive: Light Footsteps & High Speed]",
        dialogue_looey: "Looey selected! [Passive: Wider Vision Radius]",
        dialogue_blot: "Blot selected! [Passive: Stealth - Monsters move slower]",
        ichor_get: "Picked up Ichor Canister! ",
        key_get: "Obtained Elevator Keycard! Escape through the elevator!",
        locked_door: "Elevator is LOCKED! Find the Keycard first!",
        game_over: "A TWISTED TOON CAUGHT YOU! GAME OVER! Press [R] to Restart.",
        win_msg: "YOU ESCAPED GARDENVIEW! YOU SURVIVED!"
    },
    VIE: {
        title: "GARDENVIEW - 8-BIT MINIGAME",
        banners: ["C Ứ U . H Ọ . V Ớ I", "G I Ú P . T Ô I", "Đ I . T H E O . T Ô I", "C HẠ Y . Đ I"],
        dialogue_start: "Dùng WASD/Mũi tên để đi. Phím [1][2][3] đổi nhân vật. Nhặt 3 Bình Ichor & Thẻ Thang Máy!",
        dialogue_yatta: "Đã chọn Yatta! [Nội tại: Tốc độ di chuyển nhanh]",
        dialogue_looey: "Đã chọn Looey! [Nội tại: Tầm nhìn rộng hơn]",
        dialogue_blot: "Đã chọn Blot! [Nội tại: Tàng hình - Quái di chuyển chậm]",
        ichor_get: "Đã nhặt được Bình Ichor! ",
        key_get: "Đã lấy Thẻ Thang Máy! Hãy chạy ngay ra Thang Máy!",
        locked_door: "Cửa Thang Máy đang KHÓA! Hãy tìm Thẻ Từ trước!",
        game_over: "BẠN ĐÃ BỊ TWISTED BẮT! GAME OVER! Bấm [R] để chơi lại.",
        win_msg: "BẠN ĐÃ THOÁT KHỎI GARDENVIEW THÀNH CÔNG!"
    }
};

// Player Object
const player = {
    x: 80,
    y: 200,
    size: 24,
    speed: 3,
    direction: 'down'
};

// Monsters (Twisted Animatronics in FNAF style)
const monsters = [
    { x: 380, y: 120, vx: 1.2, vy: 0, dir: 1, type: 'purple_guy' },
    { x: 550, y: 280, vx: 0, vy: 1.5, dir: 1, type: 'puppet' }
];

// Collectibles
const items = [
    { x: 220, y: 80, type: 'ichor', collected: false },
    { x: 480, y: 340, type: 'ichor', collected: false },
    { x: 680, y: 100, type: 'ichor', collected: false },
    { x: 350, y: 350, type: 'keycard', collected: false }
];

// Map Layout Walls (FNAF Minigame Floor Grid)
const walls = [
    // Outer Border
    {x: 0, y: 0, w: 800, h: 20},
    {x: 0, y: 420, w: 800, h: 20},
    {x: 0, y: 0, w: 20, h: 440},
    {x: 780, y: 0, w: 20, h: 440},
    // Inner Room Walls
    {x: 160, y: 20, w: 20, h: 160},
    {x: 160, y: 260, w: 20, h: 160},
    {x: 440, y: 20, w: 20, h: 220},
    {x: 440, y: 300, w: 180, h: 20},
    {x: 620, y: 160, w: 180, h: 20}
];

// Elevator Door Target
const elevatorDoor = { x: 720, y: 220, w: 60, h: 80 };

// Keys State
const keys = {};

window.addEventListener('keydown', (e) => {
    initAudio();
    keys[e.code] = true;
    if (e.code === 'Digit1') switchChar('yatta');
    if (e.code === 'Digit2') switchChar('looey');
    if (e.code === 'Digit3') switchChar('blot');
    if (e.code === 'KeyR') resetGame();
});

window.addEventListener('keyup', (e) => {
    keys[e.code] = false;
});

function toggleLanguage() {
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    document.getElementById("title-text").innerText = strings[currentLang].title;
    updateDialogue(strings[currentLang].dialogue_start);
}

function switchChar(char) {
    activeChar = char;
    document.querySelectorAll('.char-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`btn-${char}`).classList.add('active');

    if (char === 'yatta') {
        player.speed = 3.8;
        updateDialogue(strings[currentLang].dialogue_yatta);
    } else if (char === 'looey') {
        player.speed = 3.0;
        updateDialogue(strings[currentLang].dialogue_looey);
    } else if (char === 'blot') {
        player.speed = 2.6;
        updateDialogue(strings[currentLang].dialogue_blot);
    }
}

function updateDialogue(text) {
    document.getElementById("dialogue-text").innerText = text;
}

function resetGame() {
    player.x = 80; player.y = 200;
    ichorCollected = 0;
    hasKeycard = false;
    items.forEach(i => i.collected = false);
    document.getElementById("ichor-count").innerText = "0";
    document.getElementById("key-status").innerText = currentLang === 'ENG' ? "NO" : "CHƯA";
    updateDialogue(strings[currentLang].dialogue_start);
}

// Check AABB Collision
function checkCollision(rect1, rect2) {
    return rect1.x < rect2.x + rect2.w &&
           rect1.x + rect1.size > rect2.x &&
           rect1.y < rect2.y + rect2.h &&
           rect1.y + rect1.size > rect2.y;
}

// Generate CRT Static Noise
function renderStatic() {
    const imgData = staticCtx.createImageData(400, 220);
    const buffer = new Uint32Array(imgData.data.buffer);
    for (let i = 0; i < buffer.length; i++) {
        if (Math.random() < 0.1) {
            buffer[i] = 0xffffffff;
        }
    }
    staticCtx.putImageData(imgData, 0, 0);
}

// Main Game Loop
let isGameOver = false;

function gameLoop() {
    renderStatic();

    // Clear Canvas
    ctx.fillStyle = "#050308";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw FNAF Black/Purple Checkered Floor Tiles
    const tileSize = 40;
    for (let x = 0; x < canvas.width; x += tileSize) {
        for (let y = 0; y < canvas.height; y += tileSize) {
            if (((x / tileSize) + (y / tileSize)) % 2 === 0) {
                ctx.fillStyle = "#12081c";
                ctx.fillRect(x, y, tileSize, tileSize);
            }
        }
    }

    if (!isGameOver) {
        // Player Movement Logic
        let dx = 0; let dy = 0;
        if (keys['KeyA'] || keys['ArrowLeft']) { dx = -player.speed; player.direction = 'left'; }
        if (keys['KeyD'] || keys['ArrowRight']) { dx = player.speed; player.direction = 'right'; }
        if (keys['KeyW'] || keys['ArrowUp']) { dy = -player.speed; player.direction = 'up'; }
        if (keys['KeyS'] || keys['ArrowDown']) { dy = player.speed; player.direction = 'down'; }

        if (dx !== 0 || dy !== 0) {
            if (Math.random() < 0.1) playStepSound();
        }

        // Wall Collision Prediction
        let nextX = player.x + dx;
        let nextY = player.y + dy;
        let canMoveX = true;
        let canMoveY = true;

        walls.forEach(w => {
            if (nextX < w.x + w.w && nextX + player.size > w.x && player.y < w.y + w.h && player.y + player.size > w.y) canMoveX = false;
            if (player.x < w.x + w.w && player.x + player.size > w.x && nextY < w.y + w.h && nextY + player.size > w.y) canMoveY = false;
        });

        if (canMoveX) player.x = nextX;
        if (canMoveY) player.y = nextY;

        // Collectibles Collision
        items.forEach(item => {
            if (!item.collected && checkCollision(player, {x: item.x, y: item.y, w: 20, h: 20})) {
                item.collected = true;
                playPickupSound();
                if (item.type === 'ichor') {
                    ichorCollected++;
                    document.getElementById("ichor-count").innerText = ichorCollected;
                    updateDialogue(strings[currentLang].ichor_get + `(${ichorCollected}/3)`);
                } else if (item.type === 'keycard') {
                    hasKeycard = true;
                    document.getElementById("key-status").innerText = currentLang === 'ENG' ? "YES" : "CÓ";
                    updateDialogue(strings[currentLang].key_get);
                }
            }
        });

        // Elevator Door Interaction
        if (checkCollision(player, elevatorDoor)) {
            if (hasKeycard && ichorCollected >= 3) {
                updateDialogue(strings[currentLang].win_msg);
                playPickupSound();
            } else {
                updateDialogue(strings[currentLang].locked_door);
            }
        }
    }

    // Draw Walls
    ctx.fillStyle = "#2a1b3d";
    walls.forEach(w => {
        ctx.fillRect(w.x, w.y, w.w, w.h);
        ctx.fillStyle = "#4a2c6d";
        ctx.fillRect(w.x + 2, w.y + 2, w.w - 4, w.h - 4);
        ctx.fillStyle = "#2a1b3d";
    });

    // Draw Elevator Door
    ctx.fillStyle = hasKeycard ? "#4caf50" : "#d32f2f";
    ctx.fillRect(elevatorDoor.x, elevatorDoor.y, elevatorDoor.w, elevatorDoor.h);
    ctx.fillStyle = "#000";
    ctx.font = "8px 'Press Start 2P'";
    ctx.fillText("EXIT", elevatorDoor.x + 10, elevatorDoor.y + 45);

    // Draw Items (FNAF Style Pixel Items)
    items.forEach(item => {
        if (!item.collected) {
            if (item.type === 'ichor') {
                ctx.fillStyle = "#00e676"; // Neon Green Ichor
                ctx.fillRect(item.x, item.y, 16, 20);
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(item.x + 4, item.y + 4, 8, 4);
            } else if (item.type === 'keycard') {
                ctx.fillStyle = "#ffeb3b"; // Yellow Keycard
                ctx.fillRect(item.x, item.y, 20, 14);
                ctx.fillStyle = "#000";
                ctx.fillRect(item.x + 12, item.y + 3, 4, 8);
            }
        }
    });

    // Draw Monster (Twisted Glitch Animatronics)
    monsters.forEach(m => {
        if (!isGameOver) {
            let speedMult = activeChar === 'blot' ? 0.6 : 1.0;
            if (m.type === 'purple_guy') {
                m.x += m.vx * m.dir * speedMult;
                if (m.x > 410 || m.x < 190) m.dir *= -1;
            } else {
                m.y += m.vy * m.dir * speedMult;
                if (m.y > 380 || m.y < 260) m.dir *= -1;
            }

            // Monster vs Player Collision (Jumpscare Trigger)
            if (checkCollision(player, {x: m.x, y: m.y, w: 26, h: 32})) {
                isGameOver = true;
                playGlitchJumpscareSound();
                updateDialogue(strings[currentLang].game_over);
            }
        }

        // Draw Monster 8-Bit Pixel Sprite
        ctx.fillStyle = m.type === 'purple_guy' ? "#6a1b9a" : "#e0e0e0";
        ctx.fillRect(m.x, m.y, 26, 32);
        // Eyes
        ctx.fillStyle = "#ff0000";
        ctx.fillRect(m.x + 4, m.y + 6, 6, 6);
        ctx.fillRect(m.x + 16, m.y + 6, 6, 6);
    });

    // Draw 8-Bit Player Character Sprite
    if (activeChar === 'yatta') ctx.fillStyle = "#ffb74d"; // Orange Yatta
    else if (activeChar === 'looey') ctx.fillStyle = "#fff176"; // Yellow Looey
    else ctx.fillStyle = "#78909c"; // Dark Blot

    ctx.fillRect(player.x, player.y, player.size, player.size);

    // Player Pixel Eyes
    ctx.fillStyle = "#ffffff";
    let eyeOffX = player.direction === 'left' ? 2 : player.direction === 'right' ? 12 : 6;
    ctx.fillRect(player.x + eyeOffX, player.y + 4, 4, 4);
    ctx.fillRect(player.x + eyeOffX + 6, player.y + 4, 4, 4);

    // Draw Dark Vision Radius (FNAF Flashlight Effect - Bigger for Looey)
    let visionRadius = activeChar === 'looey' ? 180 : 120;
    const grad = ctx.createRadialGradient(
        player.x + 12, player.y + 12, 20,
        player.x + 12, player.y + 12, visionRadius
    );
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(0,0,0,0.92)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // FNAF Banner Cycle
    bannerTimer++;
    if (bannerTimer % 180 === 0) {
        const bList = strings[currentLang].banners;
        bannerText = bList[Math.floor(Math.random() * bList.length)];
        document.getElementById("fnaf-banner").innerText = bannerText;
    }

    requestAnimationFrame(gameLoop);
}

// Touch control bindings
document.getElementById("btn-up").addEventListener('touchstart', () => keys['KeyW'] = true);
document.getElementById("btn-up").addEventListener('touchend', () => keys['KeyW'] = false);
document.getElementById("btn-down").addEventListener('touchstart', () => keys['KeyS'] = true);
document.getElementById("btn-down").addEventListener('touchend', () => keys['KeyS'] = false);
document.getElementById("btn-left").addEventListener('touchstart', () => keys['KeyA'] = true);
document.getElementById("btn-left").addEventListener('touchend', () => keys['KeyA'] = false);
document.getElementById("btn-right").addEventListener('touchstart', () => keys['KeyD'] = true);
document.getElementById("btn-right").addEventListener('touchend', () => keys['KeyD'] = false);

// Start Game Loop
gameLoop();
</script>
</body>
</html>
"""

# Render full Streamlit frame
components.html(game_code, height=620)
