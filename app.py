import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Escape Gardenview - Floor 1",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Giao diện tối giản
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

fnaf_mario_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gardenview - Floor 1</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
            background-color: #05020a;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        #game-box {
            position: relative;
            width: 800px;
            height: 560px;
            background: #000;
            border: 4px solid #4a148c;
            box-shadow: 0 0 30px rgba(138, 43, 226, 0.4);
            display: flex;
            flex-direction: column;
        }
        #top-ui {
            height: 36px;
            background: #0a0512;
            border-bottom: 2px solid #4a148c;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 12px;
            z-index: 10;
        }
        .title { color: #d84315; font-weight: bold; font-size: 13px; letter-spacing: 1px; }
        .btn-lang {
            background: #1a0033; color: #ea80fc; border: 1px solid #ab47bc;
            padding: 3px 8px; font-size: 11px; cursor: pointer; border-radius: 3px;
        }
        #canvas-holder {
            position: relative;
            width: 800px;
            height: 380px;
            background: #000;
        }
        canvas { display: block; width: 100%; height: 100%; image-rendering: pixelated; }
        #crt-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
        }
        #dialogue-area {
            height: 144px;
            background: #090510;
            border-top: 3px solid #4a148c;
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            position: relative;
        }
        #dialogue-text { color: #00e676; font-size: 12px; line-height: 1.5; width: 660px; }
        #speaker { color: #ffb74d; font-weight: bold; font-size: 14px; margin-bottom: 4px; }
        #char-hud {
            position: absolute; top: 10px; left: 10px; display: flex; gap: 6px; z-index: 5;
        }
        .hud-card {
            background: #120a1c; border: 1px solid #4a148c; padding: 3px 6px;
            font-size: 10px; color: #888; cursor: pointer; border-radius: 3px;
        }
        .hud-card.active { border-color: #ffb74d; color: #fff; background: #311b92; }
    </style>
</head>
<body>

<div id="game-box">
    <div id="top-ui">
        <div class="title">FLOOR 1: GARDENVIEW ENTRANCE (FNAF-MARIO STYLE)</div>
        <button class="btn-lang" onclick="toggleLang()">VIE / ENG</button>
    </div>

    <div id="canvas-holder">
        <canvas id="gameCanvas" width="800" height="380"></canvas>
        <div id="crt-overlay"></div>
        <div id="char-hud">
            <div class="hud-card active" id="c-yatta" onclick="setChar('yatta')">[1] YATTA</div>
            <div class="hud-card" id="c-looey" onclick="setChar('looey')">[2] LOOEY</div>
            <div class="hud-card" id="c-blot" onclick="setChar('blot')">[3] BLOT</div>
        </div>
    </div>

    <div id="dialogue-area">
        <div>
            <div id="speaker">SYSTEM</div>
            <div id="dialogue-text">Use [A/D] to move, [W/Space] to JUMP, [1][2][3] to switch Toon! Collect 3 Ichor Canisters to unlock Elevator!</div>
        </div>
    </div>
</div>

<script>
let lang = 'ENG';
let activeChar = 'yatta';

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game State (Mario Platformer Logic)
let player = {
    x: 40, y: 280, w: 22, h: 32,
    vx: 0, vy: 0,
    speed: 3, jumpPower: -9.5,
    grounded: false, facing: 'right'
};

let items = [
    { x: 220, y: 220, w: 12, h: 16, collected: false, type: 'ichor' },
    { x: 450, y: 150, w: 12, h: 16, collected: false, type: 'ichor' },
    { x: 680, y: 220, w: 12, h: 16, collected: false, type: 'ichor' }
];

let elevator = { x: 730, y: 260, w: 40, h: 60, open: false };

// 8-bit Platforms (Bệ đứng kiểu Mario / FNAF)
let platforms = [
    { x: 0, y: 320, w: 800, h: 60 },   // Sàn nhà chính
    { x: 180, y: 250, w: 100, h: 12 },  // Bệ 1
    { x: 380, y: 190, w: 120, h: 12 },  // Bệ 2
    { x: 630, y: 250, w: 100, h: 12 }   // Bệ 3
];

let ichorCount = 0;
const keys = { left: false, right: false, up: false };

window.addEventListener('keydown', e => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    if (e.code === 'KeyW' || e.code === 'Space' || e.code === 'ArrowUp') {
        if (player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
        }
    }
    if (e.code === 'Digit1') setChar('yatta');
    if (e.code === 'Digit2') setChar('looey');
    if (e.code === 'Digit3') setChar('blot');
});

window.addEventListener('keyup', e => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = false;
});

function setChar(c) {
    activeChar = c;
    document.querySelectorAll('.hud-card').forEach(el => el.classList.remove('active'));
    document.getElementById(`c-${c}`).classList.add('active');
    
    // Đặc tính nhân vật
    if (c === 'yatta') { player.speed = 3.2; player.jumpPower = -10; }
    else if (c === 'looey') { player.speed = 4.0; player.jumpPower = -8.8; }
    else if (c === 'blot') { player.speed = 2.8; player.jumpPower = -9.0; }
    
    updateText();
}

function toggleLang() {
    lang = lang === 'ENG' ? 'VIE' : 'ENG';
    updateText();
}

function updateText() {
    const txt = {
        ENG: `[CHAR: ${activeChar.toUpperCase()}] Collect all 3 Ichor Canisters! (${ichorCount}/3). ${elevator.open ? "ELEVATOR UNLOCKED! RUN TO THE DOOR!" : ""}`,
        VIE: `[NHÂN VẬT: ${activeChar.toUpperCase()}] Thu thập đủ 3 bình Ichor! (${ichorCount}/3). ${elevator.open ? "CỬA THANG MÁY ĐÃ MỞ! CHẠY VỀ CỬA MAU!" : ""}`
    };
    document.getElementById('speaker').innerText = activeChar.toUpperCase();
    document.getElementById('dialogue-text').innerText = txt[lang];
}

function loop() {
    // Di chuyển
    if (keys.left) { player.vx = -player.speed; player.facing = 'left'; }
    else if (keys.right) { player.vx = player.speed; player.facing = 'right'; }
    else { player.vx = 0; }

    player.vy += 0.45; // Trọng lực
    player.x += player.vx;
    player.y += player.vy;

    // Va chạm Bệ đứng (Platform Collision)
    player.grounded = false;
    platforms.forEach(p => {
        if (player.x + player.w > p.x && player.x < p.x + p.w &&
            player.y + player.h >= p.y && player.y + player.h <= p.y + p.h + player.vy) {
            player.y = p.y - player.h;
            player.vy = 0;
            player.grounded = true;
        }
    });

    // Giới hạn màn hình
    if (player.x < 0) player.x = 0;
    if (player.x + player.w > 800) player.x = 800 - player.w;

    // Nhặt đồ (Ichor)
    items.forEach(it => {
        if (!it.collected && player.x < it.x + it.w && player.x + player.w > it.x &&
            player.y < it.y + it.h && player.y + player.h >
