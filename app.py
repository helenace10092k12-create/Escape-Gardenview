import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Escape Gardenview - Circus Trio",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Escape Gardenview: Halloween Special</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
            background-color: #030105;
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
            height: 600px;
            background: #000;
            border: 4px solid #512da8;
            box-shadow: 0 0 35px rgba(81, 45, 168, 0.6);
            display: flex;
            flex-direction: column;
        }
        #top-ui {
            height: 40px;
            background: #0b0514;
            border-bottom: 2px solid #512da8;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 12px;
            z-index: 20;
        }
        .title { color: #ff7043; font-weight: bold; font-size: 11px; letter-spacing: 1px; }
        .ui-right-group { display: flex; gap: 6px; align-items: center; }
        .hud-buttons { display: flex; gap: 4px; }
        .toon-btn {
            background: #1a0b2e; color: #d1c4e9; border: 1px solid #7c4dff;
            padding: 3px 6px; font-size: 10px; cursor: pointer; border-radius: 3px;
        }
        .toon-btn.active { background: #651fff; color: #fff; font-weight: bold; }
        .lang-btn {
            background: #311b92; color: #ffeb3b; border: 1px solid #ab47bc;
            padding: 3px 6px; font-size: 10px; cursor: pointer; border-radius: 3px; font-weight: bold;
        }
        
        #canvas-holder {
            position: relative;
            width: 800px;
            height: 560px;
            background: #05020a;
        }
        canvas { display: block; width: 100%; height: 100%; image-rendering: pixelated; }
        
        #crt-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%);
            background-size: 100% 4px;
        }

        /* BỐ CỤC KHUNG CHAT SỬ DỤNG ẢNH BỒ VẼ NỔI TRÊN MÀN HÌNH GAME */
        #looey-dialogue-overlay {
            position: absolute;
            bottom: 0px;
            left: 0px;
            width: 800px;
            height: 300px;
            z-index: 50;
            display: none;
            pointer-events: none;
        }

        /* Ảnh Looey Pixel do bồ vẽ nhô từ dưới lên */
        #looey-pixel-canvas {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }

        /* Hộp chứa văn bản lọt lòng trong ô màu vàng của bức ảnh Looey */
        #looey-text-box {
            position: absolute;
            bottom: 30px;
            left: 170px;
            width: 450px;
            height: 80px;
            z-index: 60;
            padding: 8px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            pointer-events: auto;
        }

        #looey-text {
            color: #231205; /* Màu chữ tối hài hòa với ô vàng của bức vẽ */
            font-weight: bold;
            font-size: 12px;
            line-height: 1.35;
            font-family: 'Courier New', monospace;
        }

        .dialogue-btns { display: flex; justify-content: flex-end; }
        .action-btn {
            background: #311b92; color: #ffeb3b; border: 2px solid #ab47bc;
            padding: 2px 8px; font-size: 10px; cursor: pointer; border-radius: 4px; font-weight: bold;
        }
        .action-btn:hover { background: #512da8; color: #fff; }

        /* Khung thoại thường dùng cho Dẫn chuyện/Hệ thống */
        #normal-dialogue-box {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 720px;
            height: 110px;
            background: rgba(8, 3, 18, 0.95);
            border: 3px solid #7c4dff;
            border-radius: 8px;
            padding: 10px 16px;
            z-index: 40;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        #normal-speaker { color: #ffb74d; font-weight: bold; font-size: 11px; margin-bottom: 2px; }
        #normal-text { color: #00e676; font-size: 11px; line-height: 1.3; }
    </style>
</head>
<body>

<div id="game-box">
    <div id="top-ui">
        <div class="title" id="game-title">GARDENVIEW: HALLOWEEN ESCAPE</div>
        <div class="ui-right-group">
            <div class="hud-buttons">
                <button class="toon-btn" id="btn-yatta" onclick="switchCharacter('yatta')">[1] Yatta</button>
                <button class="toon-btn" id="btn-looey" onclick="switchCharacter('looey')">[2] Looey</button>
                <button class="toon-btn" id="btn-blot" onclick="switchCharacter('blot')">[3] Blot</button>
                <button class="toon-btn active" id="btn-trio" onclick="switchCharacter('trio')">[4] Trio</button>
            </div>
            <button class="lang-btn" id="lang-btn" onclick="toggleLanguage()">ENG / VIE</button>
        </div>
    </div>

    <div id="canvas-holder">
        <canvas id="gameCanvas" width="800" height="560"></canvas>
        <div id="crt-overlay"></div>
    </div>

    <!-- KHUNG THOẠI LOOEY TÍCH HỢP BỨC TRANH PIXEL CỦA BỒ -->
    <div id="looey-dialogue-overlay">
        <canvas id="looey-pixel-canvas" width="800" height="300"></canvas>
        <div id="looey-text-box">
            <div id="looey-text">My balloons almost popped right at the finale! Haha!</div>
            <div class="dialogue-btns">
                <button class="action-btn" onclick="nextLine()">Next [Space] ></button>
            </div>
        </div>
    </div>

    <!-- KHUNG THOẠI THƯỜNG -->
    <div id="normal-dialogue-box" style="display: none;">
        <div>
            <div id="normal-speaker">NARRATOR</div>
            <div id="normal-text">...</div>
        </div>
        <div class="dialogue-btns">
            <button class="action-btn" onclick="nextLine()">Next [Space] ></button>
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// VẼ LẠI BỨC TRANH PIXELART LOOEY CỦA BỒ LÊN CANVAS CHUẨN XÁC NÉT VẼ
const looeyCanvas = document.getElementById('looey-pixel-canvas');
const lCtx = looeyCanvas.getContext('2d');

function renderLooeyPixelArt() {
    lCtx.clearRect(0, 0, 800, 300);

    lCtx.save();
    lCtx.translate(120, 150);

    // 1. Tai bóng bay xanh lá & tím
    lCtx.fillStyle = '#66bb6a'; lCtx.fillRect(-35, -110, 30, 45); lCtx.fillRect(-30, -120, 20, 10);
    lCtx.fillStyle = '#ab47bc'; lCtx.fillRect(5, -110, 30, 45); lCtx.fillRect(10, -120, 20, 10);

    // 2. Đầu vàng chanh & Chi tiết mặt
    lCtx.fillStyle = '#ffee58'; lCtx.fillRect(-45, -65, 90, 65);
    
    // Mắt to tròn long lanh
    lCtx.fillStyle = '#000'; lCtx.fillRect(-32, -55, 22, 35); lCtx.fillRect(10, -55, 22, 35);
    lCtx.fillStyle = '#fff'; lCtx.fillRect(-28, -50, 6, 12); lCtx.fillRect(14, -50, 6, 12);

    // Má trái tím, má phải xanh lá & Mũi đỏ tròn
    lCtx.fillStyle = '#ab47bc'; lCtx.fillRect(-42, -25, 12, 12);
    lCtx.fillStyle = '#66bb6a'; lCtx.fillRect(30, -25, 12, 12);
    lCtx.fillStyle = '#ff1744'; lCtx.fillRect(-8, -28, 16, 14);

    // Miệng răng hề
    lCtx.fillStyle = '#fff'; lCtx.fillRect(-15, -8, 30, 10);
    lCtx.fillStyle = '#000'; lCtx.fillRect(-15, -8, 30, 2); lCtx.fillRect(-5, -8, 2, 10); lCtx.fillRect(5, -8, 2, 10);

    // Khăn quàng chấm bi
    lCtx.fillStyle = '#fff'; lCtx.fillRect(-40, 0, 80, 40);
    lCtx.fillStyle = '#ab47bc'; lCtx.fillRect(-25, 10, 12, 12); lCtx.fillRect(15, 20, 10, 10);
    lCtx.fillStyle = '#66bb6a'; lCtx.fillRect(10, 8, 12, 12); lCtx.fillRect(-20, 24, 10, 10);

    lCtx.restore();

    // 3. Khung chứa lời thoại màu vàng cam nằm đè phía dưới
    lCtx.fillStyle = '#e5c453';
    lCtx.strokeStyle = '#2b1b09';
    lCtx.lineWidth = 5;
    
    lCtx.beginPath();
    lCtx.roundRect(150, 180, 520, 100, 12);
    lCtx.fill();
    lCtx.stroke();
}
renderLooeyPixelArt();

let currentLang = 'ENG'; 
let currentStep = 0;
let activeChar = 'trio'; 
let gamePhase = 'INTRO_DIALOGUE';

let yattaPos = { x: 320, y: 450, vx: 0, vy: 0, grounded: true };
let looeyPos = { x: 360, y: 450, vx: 0, vy: 0, grounded: true };
let blotPos  = { x: 400, y: 450, vx: 0, vy: 0, grounded: true };

let speed = 3.5;
let jumpPower = -9;
const keys = { left: false, right: false };

window.addEventListener('keydown', (e) => {
    if (gamePhase === 'INTRO_DIALOGUE' || gamePhase === 'BLACKOUT_TALK') {
        if (e.code === 'Space') nextLine();
        return;
    }

    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    
    if (e.code === 'KeyW' || e.code === 'ArrowUp') {
        if (activeChar === 'yatta' && yattaPos.grounded) { yattaPos.vy = jumpPower; yattaPos.grounded = false; }
        if (activeChar === 'looey' && looeyPos.grounded) { looeyPos.vy = jumpPower; looeyPos.grounded = false; }
        if (activeChar === 'blot'  && blotPos.grounded)  { blotPos.vy = jumpPower; blotPos.grounded = false; }
        if (activeChar === 'trio') {
            if (yattaPos.grounded) { yattaPos.vy = jumpPower; yattaPos.grounded = false; }
            if (looeyPos.grounded) { looeyPos.vy = jumpPower; looeyPos.grounded = false; }
            if (blotPos.grounded)  { blotPos.vy = jumpPower; blotPos.grounded = false; }
        }
    }
    
    if (e.code === 'Space') nextLine();
    if (e.code === 'KeyE') {
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (gamePhase === 'DRESSING_ROOM' && leadX < 140) {
            gamePhase = 'BLACKOUT_TALK';
            currentStep = 5; 
            updateDialogue();
        }
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = false;
});

const introScript = {
    ENG: [
        { speaker: "NARRATOR", text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to rest." },
        { speaker: "YATTA", text: "Whew... that was a blast today! The Toon crowd was so energetic." },
        { speaker: "LOOEY", text: "My balloons almost popped right at the finale! Haha!" },
        { speaker: "BLOT", text: "Nods silently, smiling gently in the corner of the room." },
        { speaker: "SYSTEM", text: "Interact with the door: Move near the dressing room door and press [E]." }
    ],
    VIE: [
        { speaker: "DẪN CHUYỆN", text: "Buổi biểu diễn vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ nghỉ ngơi." },
        { speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê." },
        { speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", text: "Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng." },
        { speaker: "HỆ THỐNG", text: "Nhiệm vụ: Di chuyển lại gần cửa phòng thay đồ và nhấn [E]." }
    ]
};

function toggleLanguage() {
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    document.getElementById('lang-btn').innerText = currentLang === 'ENG' ? 'ENG / VIE' : 'VIE / ENG';
    updateDialogue();
}

function switchCharacter(char) {
    activeChar = char;
    document.querySelectorAll('.toon-btn').forEach(b => b.classList.remove('active'));
    let btnId = char === 'yatta' ? 'btn-yatta' : char === 'looey' ? 'btn-looey' : char === 'blot' ? 'btn-blot' : 'btn-trio';
    document.getElementById(btnId).classList.add('active');
}

function nextLine() {
    const script = intro
