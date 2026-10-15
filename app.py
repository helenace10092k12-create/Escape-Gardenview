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
        .ui-right-group {
            display: flex;
            gap: 6px;
            align-items: center;
        }
        .hud-buttons {
            display: flex;
            gap: 4px;
        }
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
            height: 360px;
            background: #05020a;
        }
        canvas { display: block; width: 100%; height: 100%; image-rendering: pixelated; }
        
        #crt-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%);
            background-size: 100% 4px;
        }

        #info-popup {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 5, 30, 0.95);
            border: 2px solid #00e676;
            padding: 8px 16px;
            border-radius: 6px;
            text-align: center;
            z-index: 30;
            display: none;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.5);
        }
        #info-title { color: #00e676; font-size: 12px; font-weight: bold; margin-bottom: 2px; }
        #info-desc { color: #e0f2f1; font-size: 10px; }

        /* KHUNG CHAT */
        #dialogue-area {
            height: 200px;
            background: #080312;
            border-top: 3px solid #512da8;
            padding: 12px 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }

        #portrait-box {
            position: absolute;
            left: 20px;
            top: -125px;
            width: 140px;
            height: 140px;
            background: #0b0514;
            border: 3px solid #7c4dff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(124, 77, 255, 0.6);
        }
        #portrait-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            image-rendering: pixelated; 
        }

        #speaker-tag {
            position: absolute;
            right: 20px;
            top: -26px;
            background: #311b92;
            border: 2px solid #7c4dff;
            color: #ffb74d;
            font-weight: bold;
            font-size: 12px;
            padding: 3px 12px;
            border-radius: 4px;
        }

        #dialogue-text { color: #00e676; font-size: 12px; line-height: 1.5; height: 70px; margin-top: 10px; }
        
        .dialogue-btns {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        .action-btn {
            background: #311b92; color: #ede7f6; border: 1px solid #7c4dff;
            padding: 4px 12px; font-size: 11px; cursor: pointer; border-radius: 4px;
        }
        .action-btn:hover { background: #512da8; }
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
        <canvas id="gameCanvas" width="800" height="360"></canvas>
        <div id="crt-overlay"></div>
        <div id="info-popup">
            <div id="info-title">CHARACTER INFO</div>
            <div id="info-desc">Description here...</div>
        </div>
    </div>

    <div id="dialogue-area">
        <div id="portrait-box">
            <img id="portrait-img" src="YOUR_IMAGE_URL_HERE" alt="Looey Sketch">
        </div>
        <div id="speaker-tag">NARRATOR</div>
        <div>
            <div id="dialogue-text">Loading introduction...</div>
        </div>
        <div class="dialogue-btns">
            <button class="action-btn" id="next-btn" onclick="nextLine()">Next [Space] ></button>
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let currentLang = 'ENG'; 
let currentStep = 0;
let activeChar = 'trio'; 
let popupTimer = null;
let gamePhase = 'DRESSING_ROOM'; 

let yattaPos = { x: 320, y: 290, vx: 0, vy: 0, grounded: true };
let looeyPos = { x: 360, y: 290, vx: 0, vy: 0, grounded: true };
let blotPos  = { x: 400, y: 290, vx: 0, vy: 0, grounded: true };

let speed = 3.5;
let jumpPower = -9;
let redButton = { x: 0, active: false };
let portalAnimProgress = 0;

const keys = { left: false, right: false };

window.addEventListener('keydown', (e) => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    
    if (e.code === 'KeyW' || e.code === 'ArrowUp') {
        if (gamePhase !== 'PORTAL_ANIM') {
            if (activeChar === 'yatta' && yattaPos.grounded) { yattaPos.vy = jumpPower; yattaPos.grounded = false; }
            if (activeChar === 'looey' && looeyPos.grounded) { looeyPos.vy = jumpPower; looeyPos.grounded = false; }
            if (activeChar === 'blot'  && blotPos.grounded)  { blotPos.vy = jumpPower; blotPos.grounded = false; }
            if (activeChar === 'trio') {
                if (yattaPos.grounded) { yattaPos.vy = jumpPower; yattaPos.grounded = false; }
                if (looeyPos.grounded) { looeyPos.vy = jumpPower; looeyPos.grounded = false; }
                if (blotPos.grounded)  { blotPos.vy = jumpPower; blotPos.grounded = false; }
            }
        }
    }
    
    if (e.code === 'Space') {
        if (!((gamePhase === 'DRESSING_ROOM' && currentStep === 4) || (gamePhase === 'BUTTON_PHASE' && currentStep === 8))) {
            nextLine();
        }
    }

    if (e.code === 'Digit1') switchCharacter('yatta');
    if (e.code === 'Digit2') switchCharacter('looey');
    if (e.code === 'Digit3') switchCharacter('blot');
    if (e.code === 'Digit4') switchCharacter('trio');

    if (e.code === 'KeyE') {
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (gamePhase === 'DRESSING_ROOM' && currentStep === 4 && leadX < 140) {
            gamePhase = 'BLACKOUT';
            currentStep = 5; 
            updateDialogue();
        } else if (gamePhase === 'BUTTON_PHASE' && redButton.active && Math.abs(leadX - redButton.x) < 40) {
            redButton.active = false;
            gamePhase = 'PORTAL_ANIM';
            portalAnimProgress = 0;
            currentStep = 9; 
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
        { speaker: "NARRATOR", text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to the dressing room to rest after the thunderous applause." },
        { speaker: "YATTA", text: "Whew... that was a blast today! The Toon crowd was so energetic." },
        { speaker: "LOOEY", text: "My balloons almost popped right at the finale! Haha!" },
        { speaker: "BLOT", text: "Nods silently, smiling gently in the corner of the room." },
        { speaker: "SYSTEM", text: "Interact with the door: Move near the dressing room door and press [E]." },
        { speaker: "NARRATOR", text: "SLAM! Suddenly, the heavy iron door of the dressing room automatically slams shut and locks tight!" },
        { speaker: "BLOT", text: "!tuocaolb latoT !tuo tew sthgih eht... edah nawoK (Trans: Wait... The lights went out! Total blackout?!)" },
        { speaker: "YATTA", text: "Huh... what is that glowing red button right under us? A strange red button..." },
        { speaker: "SYSTEM", text: "Interact with the red button: Walk to it and press [E]." },
        { speaker: "NARRATOR", text: "WHOOSH! A swirling virtual portal opens wide! The trio desperately grabs onto furniture, swirling and getting sucked in..." },
        { speaker: "NARRATOR", text: "...And finally, they are spit out from the top-left portal into a cold, desolate place. Is this Gardenview? No... it's rundown and eerie!" },
        { speaker: "SYSTEM", text: "WELCOME TO GARDENVIEW ESCAPE GAME. COLLECT 8 GOLDEN KEYS TO FORM THE PUMPKIN KEY AND ESCAPE!" },
        { speaker: "SYSTEM", text: "Controls: [A/D] Move, [W/Up] Jump, [Space] Next Dialogue, [E] Interact, [1-4] Switch Toon." }
    ],
    VIE: [
        { speaker: "DẪN CHUYỆN", text: "Buổi biểu diễn trước các Toon vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ để nghỉ ngơi sau tiếng vỗ tay vang dội." },
        { speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê luôn." },
        { speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", text: "Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng." },
        { speaker: "HỆ THỐNG", text: "Nhiệm vụ: Di chuyển lại gần cánh cửa phòng thay đồ và nhấn [E] để tương tác." },
        { speaker: "DẪN CHUYỆN", text: "RẦM! Đột nhiên, cánh cửa sắt phòng thay đồ tự động sập đóng lại chặt cứng!" },
        { speaker: "BLOT", text: "!?tuocaolb latoT !tuo tew sthgih ehT ...ad ah nawoK (Dịch: Khoan đã... Đèn tắt hết rồi! Mất điện toàn tập rồi sao?!)" },
        { speaker: "YATTA", text: "Ơ kìa... cái gì đang phát sáng đỏ rực ngay dưới chân tụi mình thế kia? Một cái nút bấm kỳ lạ..." },
        { speaker: "HỆ THỐNG", text: "Nhiệm vụ: Di chuyển đến sát cái nút bấm và nhấn [E] để tương tác." },
        { speaker: "DẪN CHUYỆN", text: "VÉO VÉO! Một cánh cổng ảo xoáy sâu mở ra! Cả ba bám chặt vào đồ đạc, xoay vòng tròn rồi bị hút tuột vào trong..." },
        { speaker: "DẪN CHUYỆN", text: "...Và rồi, cổng ở góc trái nhả phăng cả nhóm xuống đất lạnh lẽo. Gardenview đây sao? Không... nó tồi tàn và âm u đến rợn ngáy!" },
        { speaker: "HỆ THỐNG", text: "CHÀO MỪNG ĐẾN TRÒ CHƠI TRỐN THOÁT. THU THẬP 8 CHÌA KHÓA VÀNG ĐỂ HỢP THỂ THÀNH CHÌA KHÓA BÍ NGÔ!" },
        { speaker: "HỆ THỐNG", text: "Điều khiển: [A/D] Di chuyển, [W/Up] Nhảy, [Space] Tiếp theo, [E] Tương tác, [1-4] Đổi nhân vật." }
    ]
};

function toggleLanguage() {
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    document.getElementById('lang-btn').innerText = currentLang === 'ENG' ? 'ENG / VIE' : 'VIE / ENG';
    updateDialogue();
}

function updateDialogue() {
    const data = introScript[currentLang][currentStep];
    document.getElementById('speaker-tag').innerText = data.speaker;
    document.getElementById('dialogue-text').innerText = data.text;
}

function drawPixelCharacter(x, y, type, angle, scale, isSelected) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.scale(scale, scale);

    if (isSelected && activeChar !== 'trio') {
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(0, -65);
        ctx.lineTo(-6, -75);
        ctx.lineTo(6, -75);
        ctx.closePath();
        ctx.fill();
    }

    if (type === 'yatta') {
        ctx.fillStyle = '#fff59d';
        ctx.fillRect(-12, -40, 24, 32);
        ctx.fillStyle = '#ff80ab';
        ctx.fillRect(-16, -52, 8, 14);
        ctx.fillRect(8, -52, 8, 14);
        ctx.fillStyle = '#4fc3f7';
        ctx.fillRect(-14, -49, 4, 6);
        ctx.fillRect(10, -49, 4, 6);
        ctx.fillStyle = '#4fc3f7';
        ctx.fillRect(-10, -34, 20, 16);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-9, -32, 6, 8);
        ctx.fillRect(3, -32, 6, 8);
        ctx.fillStyle = '#111111';
        ctx.fillRect(-7, -29, 3, 4);
        ctx.fillRect(5, -29, 3, 4);
        
        ctx.strokeStyle = '#ff4081';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(10, -15); ctx.quadraticCurveTo(22, -18, 30, -5);
        ctx.moveTo(10, -12); ctx.quadraticCurveTo(24, -10, 32, 2);
        ctx.moveTo(10, -9);  ctx.quadraticCurveTo(20, -2, 28, 10);
        ctx.moveTo(10, -6);  ctx.quadraticCurveTo(18, 6, 26, 16);
        ctx.stroke();

        ctx.fillStyle = '#ff80ab';
        ctx.fillRect(-12, -8, 24, 18);
        ctx.fillStyle = '#4fc3f7';
        ctx.fillRect(-8, -8, 4, 18);
        ctx.fillRect(4, -8, 4, 18);
    } 
    else if (type === 'looey') {
        ctx.fillStyle = '#ffee58';
        ctx.fillRect(-14, -38, 28, 30);
        ctx.fillStyle = '#66bb6a';
        ctx.fillRect(-10, -56, 8, 18);
        ctx.fillStyle = '#ab47bc';
        ctx.fillRect(2, -56, 8, 18);
        ctx.fillStyle = '#000000';
        ctx.fillRect(-8, -28, 4, 6);
        ctx.fillRect(4, -28, 4, 6);
        ctx.fillStyle = '#ff7043';
        ctx.fillRect(-12, -8, 24, 18);
    } 
    else if (type === 'blot') {
        ctx.fillStyle = '#37474f';
        ctx.fillRect(-12, -38, 24, 32);
        ctx.fillStyle = '#212121';
        ctx.fillRect(-12, -38, 14, 16);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(2, -30, 8, 8);
        ctx.fillStyle = '#000000';
        ctx.fillRect(5, -27, 3, 3);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-12, -8, 24, 18);
        ctx.fillStyle = '#000000';
        ctx.fillRect(-8, -8, 4, 18);
        ctx.fillRect(0, -8, 4, 18);
    }
    ctx.restore();
}

function gameLoop() {
    if (gamePhase !== 'PORTAL_ANIM' && gamePhase !== 'GARDENVIEW_SPIT') {
        let moveX = 0;
        if (keys.left) moveX = -speed;
        if (keys.right) moveX = speed;

        if (activeChar === 'trio') {
            yattaPos.vx = moveX; looeyPos.vx = moveX; blotPos.vx = moveX;
        } else if (activeChar === 'yatta') {
            yattaPos.vx = moveX; looeyPos.vx = 0; blotPos.vx = 0;
        } else if (activeChar === 'looey') {
            yattaPos.vx = 0; looeyPos.vx = moveX; blotPos.vx = 0;
        } else if (activeChar === 'blot') {
            yattaPos.vx = 0; looeyPos.vx = 0; blotPos.vx = moveX;
        }

        [yattaPos, looeyPos, blotPos].forEach(p => {
            p.vy += 0.4;
            p.x += p.vx;
            p.y += p.vy;
            if (p.y >= 290) {
                p.y = 290;
                p.vy = 0;
                p.grounded = true;
            }
            if (p.x < 20) p.x = 20;
            if (p.x > 740) p.x = 740;
        });
    }

    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#030103' : '#06030c';
    ctx.fillRect(0, 0, 800, 360);

    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#0a030f' : '#0f071a';
    for(let x = 0; x < 800; x += 40) {
        for(let y = 0; y < 380; y += 40) {
            if ((x/40 + y/40) % 2 === 0) ctx.fillRect(x, y, 40, 40);
        }
    }

    if (gamePhase === 'DRESSING_ROOM' || gamePhase === 'BLACKOUT' || gamePhase === 'BUTTON_PHASE') {
        ctx.fillStyle = '#311b92';
        ctx.fillRect(60, 140, 70, 150);
        ctx
