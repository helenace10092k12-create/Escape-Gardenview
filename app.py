import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Escape Gardenview - Circus Trio",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn bớt giao diện thừa của Streamlit để giống Game thực thụ
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

# Mã nguồn HTML5 + JS Side-View Game Engine
game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Escape Gardenview</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #050508;
            color: #e0e0e0;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            width: 800px;
            height: 600px;
            background: #000;
            border: 4px solid #332244;
            box-shadow: 0 0 25px rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
        }
        #top-bar {
            height: 40px;
            background: #110d18;
            border-bottom: 2px solid #332244;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 15px;
            z-index: 10;
        }
        .title-text {
            color: #d84315;
            font-weight: bold;
            font-size: 14px;
            letter-spacing: 1px;
        }
        .lang-btn {
            background: #281a38;
            color: #e0d0f0;
            border: 1px solid #6a1b9a;
            padding: 4px 10px;
            font-size: 12px;
            cursor: pointer;
            border-radius: 4px;
            font-family: inherit;
        }
        .lang-btn:hover {
            background: #4a148c;
        }
        #canvas-wrapper {
            position: relative;
            width: 800px;
            height: 410px;
            background: #08060c;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
            image-rendering: pixelated;
        }
        #vignette {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(circle at center, transparent 40%, rgba(0,0,0,0.85) 90%);
        }
        #dialogue-box {
            height: 150px;
            background: rgba(12, 8, 18, 0.95);
            border-top: 3px solid #4a148c;
            padding: 12px 15px;
            display: flex;
            position: relative;
        }
        #dialogue-content {
            flex: 1;
            padding-right: 120px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        #speaker-name {
            color: #ffb74d;
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        #dialogue-text {
            color: #f5f5f5;
            font-size: 13px;
            line-height: 1.4;
            min-height: 50px;
        }
        #choices-container {
            display: flex;
            gap: 10px;
            margin-top: 8px;
        }
        .choice-btn {
            background: #1a0033;
            color: #e1bee7;
            border: 1px solid #8e24aa;
            padding: 6px 12px;
            font-size: 12px;
            cursor: pointer;
            border-radius: 4px;
            font-family: inherit;
        }
        .choice-btn:hover {
            background: #4a148c;
            color: #fff;
        }
        #portrait-container {
            position: absolute;
            right: 15px;
            bottom: 10px;
            width: 110px;
            height: 130px;
            border: 2px solid #4a148c;
            background: #05020a;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #portrait-canvas {
            width: 100px;
            height: 120px;
            image-rendering: pixelated;
        }
        #hud-party {
            position: absolute;
            top: 10px;
            left: 10px;
            display: flex;
            gap: 8px;
            z-index: 5;
        }
        .party-card {
            background: rgba(15, 10, 25, 0.8);
            border: 1px solid #443355;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            color: #888;
            cursor: pointer;
        }
        .party-card.active {
            border-color: #ab47bc;
            color: #fff;
            background: rgba(60, 20, 90, 0.9);
            font-weight: bold;
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="top-bar">
        <div class="title-text">GARDENVIEW: SIDE-VIEW SURVIVAL</div>
        <button class="lang-btn" id="lang-toggle" onclick="toggleLanguage()">VIE / ENG</button>
    </div>

    <div id="canvas-wrapper">
        <canvas id="gameCanvas" width="800" height="410"></canvas>
        <div id="vignette"></div>
        <div id="hud-party">
            <div class="party-card active" id="card-yatta" onclick="switchChar('yatta')">[1] Yatta</div>
            <div class="party-card" id="card-looey" onclick="switchChar('looey')">[2] Looey</div>
            <div class="party-card" id="card-blot" onclick="switchChar('blot')">[3] Blot</div>
        </div>
    </div>

    <div id="dialogue-box">
        <div id="dialogue-content">
            <div>
                <div id="speaker-name">Yatta</div>
                <div id="dialogue-text">Loading game...</div>
            </div>
            <div id="choices-container"></div>
        </div>
        <div id="portrait-container">
            <canvas id="portrait-canvas" width="100" height="120"></canvas>
        </div>
    </div>
</div>

<script>
// Game State
let currentLang = 'ENG'; // 'ENG' or 'VIE'
let gameState = 'COMIC'; // 'COMIC' or 'SIDEVIEW'
let comicFrame = 0;
let activeChar = 'yatta'; // 'yatta', 'looey', 'blot'

// Canvas References
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const portraitCanvas = document.getElementById("portrait-canvas");
const pCtx = portraitCanvas.getContext("2d");

// Player State (Side-view Side-scroller)
let player = {
    x: 100,
    y: 280,
    vx: 0,
    vy: 0,
    width: 32,
    height: 54,
    isJumping: false,
    speed: 3.5,
    facing: 'right'
};

// Key States
const keys = { left: false, right: false, up: false };

window.addEventListener('keydown', (e) => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    if (e.code === 'KeyW' || e.code === 'Space' || e.code === 'ArrowUp') {
        keys.up = true;
        if (!player.isJumping && gameState === 'SIDEVIEW') {
            player.vy = -10; // Jump force
            player.isJumping = true;
        }
    }
    if (e.code === 'Digit1') switchChar('yatta');
    if (e.code === 'Digit2') switchChar('looey');
    if (e.code === 'Digit3') switchChar('blot');
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = false;
    if (e.code === 'KeyW' || e.code === 'Space' || e.code === 'ArrowUp') keys.up = false;
});

// Languages Database
const texts = {
    ENG: {
        speakers: { yatta: "Yatta", looey: "Looey", blot: "Blot", narrator: "Story" },
        comic: [
            { speaker: 'yatta', text: "Whew! What a show! We nailed that performance, guys!" },
            { speaker: 'looey', text: "My balloons almost popped during the finale! Ha ha!" },
            { speaker: 'narrator', text: "*SLAM!* The dressing room heavy iron door slammed shut automatically!" },
            { speaker: 'blot', text: "Wait... the lights went out. Total blackout." },
            { speaker: 'yatta', text: "A strange glowing red button appeared on the floor..." },
            { speaker: 'narrator', text: "*ZOOM!* The portal swallowed them whole down into Abandoned Gardenview!" }
        ],
        sideview: {
            intro: "Aah! My tail hurts... Where are we? Use [A/D] or [Left/Right] to move, [Space/W] to Jump, and [1][2][3] to switch characters!",
            interact_door: "The elevator door is locked tight. It needs an Elevator Keycard.",
            choices_door: ["Search locker", "Examine Ink puddle"]
        }
    },
    VIE: {
        speakers: { yatta: "Yatta", looey: "Looey", blot: "Blot", narrator: "Dẫn chuyện" },
        comic: [
            { speaker: 'yatta', text: "Phù! Buổi diễn đỉnh quá mấy bồ ơi!" },
            { speaker: 'looey', text: "Bóng bay của tui xíu nữa là nổ tung lúc hạ màn luôn á! Cười xỉu!" },
            { speaker: 'narrator', text: "*RẦM!* Cửa sắt phòng thay đồ đột ngột sập đóng lại!" },
            { speaker: 'blot', text: "Khoan đã... đèn tắt hết rồi. Tối đen như mực." },
            { speaker: 'yatta', text: "Một nút bấm màu đỏ kỳ lạ tự nhiên phát sáng trên sàn..." },
            { speaker: 'narrator', text: "*VỐOONG!* Cổng dịch chuyển hút cả ba xuống Gardenview bỏ hoang!" }
        ],
        sideview: {
            intro: "Ái da... cái đuôi của tui! Đây là đâu vậy? Dùng [A/D] để di chuyển, [W/Space] để Nhảy, [1][2][3] để đổi nhân vật!",
            interact_door: "Cửa thang máy đóng chặt rồi. Cần phải tìm Thẻ Từ Thang Máy.",
            choices_door: ["Lục tủ Locker", "Kiểm tra vũng mực"]
        }
    }
};

function toggleLanguage() {
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    updateDialogue();
}

function switchChar(char) {
    activeChar = char;
    document.querySelectorAll('.party-card').forEach(c => c.classList.remove('active'));
    document.getElementById(`card-${char}`).classList.add('active');
    drawPortrait();
    if (gameState === 'SIDEVIEW') {
        document.getElementById("speaker-name").innerText = texts[currentLang].speakers[char];
    }
}

// Draw Pixel Character Portrait
function drawPortrait() {
    pCtx.clearRect(0,0,100,120);
    pCtx.fillStyle = "#110b18";
    pCtx.fillRect(0,0,100,120);

    if (activeChar === 'yatta') {
        pCtx.fillStyle = "#ffb74d";
        pCtx.fillRect(35, 45, 30, 45); // Head
        pCtx.fillStyle = "#e91e63";
        pCtx.fillRect(25, 25, 15, 25); // Left ear/ribbon
        pCtx.fillRect(60, 25, 15, 25); // Right ear/ribbon
        pCtx.fillStyle = "#ffffff";
        pCtx.fillRect(40, 55, 8, 8); pCtx.fillRect(52, 55, 8, 8); // Eyes
        pCtx.fillStyle = "#000000";
        pCtx.fillRect(44, 57, 4, 4); pCtx.fillRect(54, 57, 4, 4);
    } else if (activeChar === 'looey') {
        pCtx.fillStyle = "#fff176";
        pCtx.fillRect(30, 40, 40, 50); // Round Head
        pCtx.fillStyle = "#81c784";
        pCtx.fillRect(25, 15, 20, 30); // Balloon 1
        pCtx.fillStyle = "#ba68c8";
        pCtx.fillRect(55, 15, 20, 30); // Balloon 2
        pCtx.fillStyle = "#000000";
        pCtx.fillRect(40, 55, 6, 6); pCtx.fillRect(54, 55, 6, 6); // Eyes
    } else if (activeChar === 'blot') {
        pCtx.fillStyle = "#424242";
        pCtx.fillRect(30, 40, 40, 50); // Dark Head
        pCtx.fillStyle = "#212121";
        pCtx.fillRect(25, 35, 25, 35); // Dripping Ink Hair/Eye cover
        pCtx.fillStyle = "#ffffff";
        pCtx.fillRect(55, 55, 10, 10); // One big eye
        pCtx.fillStyle = "#000000";
        pCtx.fillRect(58, 58, 4, 4);
    }
}

function updateDialogue() {
    const choicesComp = document.getElementById("choices-container");
    choicesComp.innerHTML = "";

    if (gameState === 'COMIC') {
        const data = texts[currentLang].comic[comicFrame];
        document.getElementById("speaker-name").innerText = texts[currentLang].speakers[data.speaker];
        document.getElementById("dialogue-text").innerText = data.text;

        const nextBtn = document.createElement("button");
        nextBtn.className = "choice-btn";
        nextBtn.innerText = currentLang === 'ENG' ? "Next [Space] >" : "Tiếp theo [Space] >";
        nextBtn.onclick = advanceComic;
        choicesComp.appendChild(nextBtn);
    } else {
        document.getElementById("speaker-name").innerText = texts[currentLang].speakers[activeChar];
        document.getElementById("dialogue-text").innerText = texts[currentLang].sideview.intro;
    }
}

function advanceComic() {
    comicFrame++;
    if (comicFrame >= texts[currentLang].comic.length) {
        gameState = 'SIDEVIEW';
        updateDialogue();
    } else {
        updateDialogue();
    }
}

// Side-View Main Game Loop
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'COMIC') {
        // Render Comic Frames
        ctx.fillStyle = "#120a1c";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.strokeStyle = "#4a148c";
        ctx.lineWidth = 6;
        ctx.strokeRect(50, 40, 700, 330);
        
        ctx.fillStyle = "#ffffff";
        ctx.font = "20px 'Courier New'";
        ctx.textAlign = "center";
        ctx.fillText(`[ COMIC FRAME ${comicFrame + 1} / 6 ]`, 400, 200);
        ctx.textAlign = "left";

    } else if (gameState === 'SIDEVIEW') {
        // Physics
        if (keys.left) { player.vx = -player.speed; player.facing = 'left'; }
        else if (keys.right) { player.vx = player.speed; player.facing = 'right'; }
        else { player.vx = 0; }

        player.vy += 0.5; // Gravity
        player.x += player.vx;
        player.y += player.vy;

        // Floor Collision
        if (player.y >= 280) {
            player.y = 280;
            player.vy = 0;
            player.isJumping = false;
        }

        // Screen Boundaries
        if (player.x < 20) player.x = 20;
        if (player.x > 740) player.x = 740;

        // Draw Side-view Background (Abandoned Gardenview Hallway)
        ctx.fillStyle = "#100c14"; ctx.fillRect(0, 0, 800, 410); // Wall
        ctx.fillStyle = "#22182b"; ctx.fillRect(0, 334, 800, 76); // Floor

        // Checkerboard tile strip on floor
        for(let i=0; i<800; i+=30) {
            ctx.fillStyle = (i/30)%2===0 ? "#2d1e3e" : "#1a1224";
            ctx.fillRect(i, 334, 30, 20);
        }

        // Background Details (Interactive Door & Lockers)
        ctx.fillStyle = "#3e2723"; ctx.fillRect(600, 180, 80, 154); // Elevator Door
        ctx.fillStyle = "#1a0e0b"; ctx.fillRect(610, 190, 60, 134);
        ctx.fillStyle = "#ffb300"; ctx.fillRect(660, 250, 6, 12); // Door handle

        // Lockers
        ctx.fillStyle = "#37474f"; ctx.fillRect(200, 200, 50, 134);
        ctx.fillStyle = "#263238"; ctx.fillRect(205, 205, 40, 124);

        // Ink Puddle
        ctx.fillStyle = "#000000";
        ctx.beginPath();
        ctx.ellipse(420, 330, 45, 8, 0, 0, Math.PI * 2);
        ctx.fill();

        // Draw Side-View Follower Party (Looey & Blot behind Yatta)
        let followerOffset = player.facing === 'right' ? -35 : 35;
        
        // Follower 2
        ctx.fillStyle = activeChar === 'blot' ? "#fff176" : "#424242";
        ctx.fillRect(player.x + followerOffset * 2, player.y + 10, 24, 44);

        // Follower 1
        ctx.fillStyle = activeChar === 'looey' ? "#ffb74d" : "#fff176";
        ctx.fillRect(player.x + followerOffset, player.y + 5, 26, 49);

        // Draw Active Leading Player Side-View Sprite
        if (activeChar === 'yatta') ctx.fillStyle = "#ffb74d";
        else if (activeChar === 'looey') ctx.fillStyle = "#fff176";
        else ctx.fillStyle = "#424242";

        ctx.fillRect(player.x, player.y, player.width, player.height); // Body
        ctx.fillStyle = "#ffffff";
        let eyeX = player.facing === 'right' ? player.x + 18 : player.x + 4;
        ctx.fillRect(eyeX, player.y + 10, 8, 8); // Eyes facing direction
        ctx.fillStyle = "#000000";
        ctx.fillRect(eyeX + (player.facing === 'right' ? 4 : 0), player.y + 12, 4, 4);
    }

    requestAnimationFrame(gameLoop);
}

// Initial setup
drawPortrait();
updateDialogue();
gameLoop();
</script>
</body>
</html>
"""

# Embed Game Component
components.html(game_code, height=620)
