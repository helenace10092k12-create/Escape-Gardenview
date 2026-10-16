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

        /* KHUNG CHAT TÍCH HỢP NGUYÊN BỨC ẢNH VẼ TAY CỦA BỒ */
        #dialogue-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 800px;
            height: 320px;
            z-index: 50;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            pointer-events: none;
        }

        /* Ảnh phác thảo đầy đủ (Looey / Yatta) */
        #sketch-bg-img {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: bottom;
            pointer-events: none;
            filter: drop-shadow(0px -5px 10px rgba(0,0,0,0.8));
        }

        /* Chữ lời thoại đè đúng vị trí lòng khung chat trong bức vẽ tay */
        #dialogue-content {
            position: relative;
            z-index: 60;
            margin: 0 40px 30px 40px;
            height: 110px;
            padding: 10px 15px;
            pointer-events: auto;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        #dialogue-text {
            color: #000000; /* Đổi màu chữ tối cho hợp nền giấy phác thảo */
            font-weight: bold;
            font-size: 13px;
            line-height: 1.4;
            font-family: 'Courier New', monospace;
        }

        .dialogue-btns { display: flex; justify-content: flex-end; }
        .action-btn {
            background: #1a0b2e; color: #00e676; border: 2px solid #7c4dff;
            padding: 4px 12px; font-size: 11px; cursor: pointer; border-radius: 4px; font-weight: bold;
        }
        .action-btn:hover { background: #512da8; color: #fff; }
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

    <!-- KHUNG THOẠI VẼ TAY POP-UP -->
    <div id="dialogue-overlay" style="display: none;">
        <img id="sketch-bg-img" src="" alt="Sketch Dialogue Overlay">
        <div id="dialogue-content">
            <div id="dialogue-text">...</div>
            <div class="dialogue-btns">
                <button class="action-btn" id="next-btn" onclick="nextLine()">Next [Space] ></button>
            </div>
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- LINK ẢNH VẼ TAY CỦA BỒ (Bồ thay URL ảnh thực tế vào đây nhé) ---
const LOOEY_CHATBOX_IMG = "LOOEY_CHATBOX_URL"; // Ảnh 1
const YATTA_CHATBOX_IMG = "YATTA_CHATBOX_URL"; // Ảnh 4

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
        { speaker: "NARRATOR", img: null, text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to rest." },
        { speaker: "YATTA", img: YATTA_CHATBOX_IMG, text: "Whew... that was a blast today! The Toon crowd was so energetic." },
        { speaker: "LOOEY", img: LOOEY_CHATBOX_IMG, text: "My balloons almost popped right at the finale! Haha!" },
        { speaker: "BLOT", img: null, text: "*Nods silently, smiling gently in the corner of the room.*" },
        { speaker: "SYSTEM", img: null, text: "Interact with the door: Move near the dressing room door and press [E]." }
    ],
    VIE: [
        { speaker: "DẪN CHUYỆN", img: null, text: "Buổi biểu diễn vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ nghỉ ngơi." },
        { speaker: "YATTA", img: YATTA_CHATBOX_IMG, text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê." },
        { speaker: "LOOEY", img: LOOEY_CHATBOX_IMG, text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", img: null, text: "*Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng.*" },
        { speaker: "HỆ THỐNG", img: null, text: "Nhiệm vụ: Di chuyển lại gần cửa phòng thay đồ và nhấn [E]." }
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
    const script = introScript[currentLang];
    currentStep++;
    if (currentStep >= script.length) {
        document.getElementById('dialogue-overlay').style.display = 'none';
        gamePhase = 'DRESSING_ROOM';
        return;
    }
    updateDialogue();
}

function updateDialogue() {
    const data = introScript[currentLang][currentStep];
    const overlay = document.getElementById('dialogue-overlay');
    const imgElem = document.getElementById('sketch-bg-img');
    const textElem = document.getElementById('dialogue-text');

    overlay.style.display = 'flex';
    textElem.innerText = `${data.speaker}: ${data.text}`;

    if (data.img && data.img !== "LOOEY_CHATBOX_URL" && data.img !== "YATTA_CHATBOX_URL") {
        imgElem.style.display = 'block';
        imgElem.src = data.img;
        textElem.style.color = "#111"; // Chữ màu đen viết trên mặt giấy
    } else {
        imgElem.style.display = 'none';
        textElem.style.color = "#00e676"; // Chữ màu xanh huỳnh quang nếu không có hình phác thảo
    }
}

function drawPixelCharacter(x, y, type) {
    ctx.save();
    ctx.translate(x, y);

    if (type === 'yatta') {
        ctx.fillStyle = '#fff59d'; ctx.fillRect(-12, -40, 24, 32);
        ctx.fillStyle = '#ff80ab'; ctx.fillRect(-16, -52, 8, 14); ctx.fillRect(8, -52, 8, 14);
    } else if (type === 'looey') {
        ctx.fillStyle = '#ffee58'; ctx.fillRect(-14, -38, 28, 30);
        ctx.fillStyle = '#66bb6a'; ctx.fillRect(-10, -56, 8, 18);
    } else if (type === 'blot') {
        ctx.fillStyle = '#37474f'; ctx.fillRect(-12, -38, 24, 32);
    }
    ctx.restore();
}

function gameLoop() {
    if (gamePhase === 'DRESSING_ROOM' || gamePhase === 'EXPLORE') {
        let moveX = 0;
        if (keys.left) moveX = -speed;
        if (keys.right) moveX = speed;

        if (activeChar === 'trio') { yattaPos.vx = moveX; looeyPos.vx = moveX; blotPos.vx = moveX; }
        else if (activeChar === 'yatta') { yattaPos.vx = moveX; looeyPos.vx = 0; blotPos.vx = 0; }
        else if (activeChar === 'looey') { yattaPos.vx = 0; looeyPos.vx = moveX; blotPos.vx = 0; }
        else if (activeChar === 'blot') { yattaPos.vx = 0; looeyPos.vx = 0; blotPos.vx = moveX; }

        [yattaPos, looeyPos, blotPos].forEach(p => {
            p.vy += 0.4; p.x += p.vx; p.y += p.vy;
            if (p.y >= 450) { p.y = 450; p.vy = 0; p.grounded = true; }
            if (p.x < 20) p.x = 20; if (p.x > 740) p.x = 740;
        });
    }

    ctx.fillStyle = '#06030c'; ctx.fillRect(0, 0, 800, 560);

    // Cửa phòng thay đồ
    if (gamePhase === 'DRESSING_ROOM') {
        ctx.fillStyle = '#311b92'; ctx.fillRect(60, 300, 70, 150);
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (leadX < 140) {
            ctx.fillStyle = '#00e676'; ctx.font = '12px Courier New'; ctx.fillText("Interact with door [E]", 45, 285);
        }
    }

    // Sàn
    ctx.fillStyle = '#281145'; ctx.fillRect(0, 450, 800, 110);
    ctx.fillStyle = '#7c4dff'; ctx.fillRect(0, 450, 800, 4);

    drawPixelCharacter(yattaPos.x, yattaPos.y, 'yatta');
    drawPixelCharacter(looeyPos.x, looeyPos.y, 'looey');
    drawPixelCharacter(blotPos.x, blotPos.y, 'blot');

    requestAnimationFrame(gameLoop);
}

updateDialogue();
gameLoop();
</script>
</body>
</html>
"""

components.html(game_code, height=620)
