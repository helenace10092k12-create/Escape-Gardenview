import streamlit as st
import streamlit.components.v1 as components
import base64

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

# ĐƯỜNG LINK RAW ẢNH PIXEL LOOEY TRÊN GITHUB CỦA BỒ 
# (Hoặc bồ có thể để file ảnh 'looey_chat.png' chung thư mục với app.py rồi mở file ra đọc mã Base64)
LOOEY_PIXEL_URL = "https://raw.githubusercontent.com/username/repo/main/1000009227.png"

game_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Escape Gardenview: Halloween Special</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
        body {{
            background-color: #030105;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }}
        #game-box {{
            position: relative;
            width: 800px;
            height: 600px;
            background: #000;
            border: 4px solid #512da8;
            box-shadow: 0 0 35px rgba(81, 45, 168, 0.6);
            display: flex;
            flex-direction: column;
        }}
        #top-ui {{
            height: 40px;
            background: #0b0514;
            border-bottom: 2px solid #512da8;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 12px;
            z-index: 20;
        }}
        .title {{ color: #ff7043; font-weight: bold; font-size: 11px; letter-spacing: 1px; }}
        .ui-right-group {{ display: flex; gap: 6px; align-items: center; }}
        .hud-buttons {{ display: flex; gap: 4px; }}
        .toon-btn {{
            background: #1a0b2e; color: #d1c4e9; border: 1px solid #7c4dff;
            padding: 3px 6px; font-size: 10px; cursor: pointer; border-radius: 3px;
        }}
        .toon-btn.active {{ background: #651fff; color: #fff; font-weight: bold; }}
        .lang-btn {{
            background: #311b92; color: #ffeb3b; border: 1px solid #ab47bc;
            padding: 3px 6px; font-size: 10px; cursor: pointer; border-radius: 3px; font-weight: bold;
        }}
        
        #canvas-holder {{
            position: relative;
            width: 800px;
            height: 560px;
            background: #05020a;
        }}
        canvas {{ display: block; width: 100%; height: 100%; image-rendering: pixelated; }}
        
        #crt-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%);
            background-size: 100% 4px;
        }}

        /* HỘP THOẠI CHÍNH XÁC NỐI NGUYÊN BỨC ẢNH PIXEL CỦA BỒ */
        #looey-dialogue-overlay {{
            position: absolute;
            bottom: 0px;
            left: 0px;
            width: 800px;
            height: 320px;
            z-index: 50;
            display: none;
            pointer-events: none;
        }}

        #looey-pixel-img {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: bottom;
            image-rendering: pixelated; /* Giữ độ nét Pixel Art chuẩn 100% */
        }}

        /* Lời thoại lọt đúng lòng ô màu vàng trong bức ảnh Looey */
        #looey-text-box {{
            position: absolute;
            bottom: 35px;
            left: 175px;
            width: 440px;
            height: 80px;
            z-index: 60;
            padding: 8px 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            pointer-events: auto;
        }}

        #looey-text {{
            color: #2a1508; /* Chữ màu nâu tím đậm hài hòa với ô vàng của Looey */
            font-weight: bold;
            font-size: 13px;
            line-height: 1.35;
            font-family: 'Courier New', monospace;
        }}

        .dialogue-btns {{ display: flex; justify-content: flex-end; }}
        .action-btn {{
            background: #311b92; color: #ffeb3b; border: 2px solid #ab47bc;
            padding: 3px 10px; font-size: 10px; cursor: pointer; border-radius: 4px; font-weight: bold;
        }}
        .action-btn:hover {{ background: #512da8; color: #fff; }}

        #normal-dialogue-box {{
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
        }}
        #normal-speaker {{ color: #ffb74d; font-weight: bold; font-size: 11px; margin-bottom: 2px; }}
        #normal-text {{ color: #00e676; font-size: 11px; line-height: 1.3; }}
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

    <!-- KHUNG THOẠI LOOEY SỬ DỤNG BỨC ẢNH PIXEL VẼ TAY THẬT -->
    <div id="looey-dialogue-overlay">
        <img id="looey-pixel-img" src="{LOOEY_PIXEL_URL}" alt="Looey Pixel Sketch">
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

let currentLang = 'ENG'; 
let currentStep = 0;
let activeChar = 'trio'; 
let gamePhase = 'INTRO_DIALOGUE';

let yattaPos = {{ x: 320, y: 450, vx: 0, vy: 0, grounded: true }};
let looeyPos = {{ x: 360, y: 450, vx: 0, vy: 0, grounded: true }};
let blotPos  = {{ x: 400, y: 450, vx: 0, vy: 0, grounded: true }};

let speed = 3.5;
let jumpPower = -9;
const keys = {{ left: false, right: false }};

window.addEventListener('keydown', (e) => {{
    if (gamePhase === 'INTRO_DIALOGUE' || gamePhase === 'BLACKOUT_TALK') {{
        if (e.code === 'Space') nextLine();
        return;
    }}

    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    
    if (e.code === 'KeyW' || e.code === 'ArrowUp') {{
        if (activeChar === 'yatta' && yattaPos.grounded) {{ yattaPos.vy = jumpPower; yattaPos.grounded = false; }}
        if (activeChar === 'looey' && looeyPos.grounded) {{ looeyPos.vy = jumpPower; looeyPos.grounded = false; }}
        if (activeChar === 'blot'  && blotPos.grounded)  {{ blotPos.vy = jumpPower; blotPos.grounded = false; }}
        if (activeChar === 'trio') {{
            if (yattaPos.grounded) {{ yattaPos.vy = jumpPower; yattaPos.grounded = false; }}
            if (looeyPos.grounded) {{ looeyPos.vy = jumpPower; looeyPos.grounded = false; }}
            if (blotPos.grounded)  {{ blotPos.vy = jumpPower; blotPos.grounded = false; }}
        }}
    }}
    
    if (e.code === 'Space') nextLine();
    if (e.code === 'KeyE') {{
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (gamePhase === 'DRESSING_ROOM' && leadX < 140) {{
            gamePhase = 'BLACKOUT_TALK';
            currentStep = 5; 
            updateDialogue();
        }}
    }}
}});

window.addEventListener('keyup', (e) => {{
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = false;
}});

const introScript = {{
    ENG: [
        {{ speaker: "NARRATOR", text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to rest." }},
        {{ speaker: "YATTA", text: "Whew... that was a blast today! The Toon crowd was so energetic." }},
        {{ speaker: "LOOEY", text: "My balloons almost popped right at the finale! Haha!" }},
        {{ speaker: "BLOT", text: "Nods silently, smiling gently in the corner of the room." }},
        {{ speaker: "SYSTEM", text: "Interact with the door: Move near the dressing room door and press [E]." }}
    ],
    VIE: [
        {{ speaker: "DẪN CHUYỆN", text: "Buổi biểu diễn vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ nghỉ ngơi." }},
        {{ speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê." }},
        {{ speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" }},
        {{ speaker: "BLOT", text: "Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng." }},
        {{ speaker: "HỆ THỐNG", text: "Nhiệm vụ: Di chuyển lại gần cửa phòng thay đồ và nhấn [E]." }}
    ]
}};

function toggleLanguage() {{
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    document.getElementById('lang-btn').innerText = currentLang === 'ENG' ? 'ENG / VIE' : 'VIE / ENG';
    updateDialogue();
}}

function switchCharacter(char) {{
    activeChar = char;
    document.querySelectorAll('.toon-btn').forEach(b => b.classList.remove('active'));
    let btnId = char === 'yatta' ? 'btn-yatta' : char === 'looey' ? 'btn-looey' : char === 'blot' ? 'btn-blot' : 'btn-trio';
    document.getElementById(btnId).classList.add('active');
}}

function nextLine() {{
    const script = introScript[currentLang];
    currentStep++;
    if (currentStep >= script.length) {{
        document.getElementById('looey-dialogue-overlay').style.display = 'none';
        document.getElementById('normal-dialogue-box').style.display = 'none';
        gamePhase = 'DRESSING_ROOM';
        return;
    }}
    updateDialogue();
}}

function updateDialogue() {{
    const data = introScript[currentLang][currentStep];
    const looeyOverlay = document.getElementById('looey-dialogue-overlay');
    const normalBox = document.getElementById('normal-dialogue-box');

    if (data.speaker === 'LOOEY') {{
        normalBox.style.display = 'none';
        looeyOverlay.style.display = 'block';
        document.getElementById('looey-text').innerText = data.text;
    }} else {{
        looeyOverlay.style.display = 'none';
        normalBox.style.display = 'flex';
        document.getElementById('normal-speaker').innerText = data.speaker;
        document.getElementById('normal-text').innerText = data.text;
    }}
}}

function drawPixelCharacter(x, y, type) {{
    ctx.save();
    ctx.translate(x, y);

    if (type === 'yatta') {{
        ctx.fillStyle = '#fff59d'; ctx.fillRect(-12, -40, 24, 32);
        ctx.fillStyle = '#ff80ab'; ctx.fillRect(-16, -52, 8, 14); ctx.fillRect(8, -52, 8, 14);
    }} else if (type === 'looey') {{
        ctx.fillStyle = '#ffee58'; ctx.fillRect(-14, -38, 28, 30);
        ctx.fillStyle = '#66bb6a'; ctx.fillRect(-10, -56, 8, 18);
    }} else if (type === 'blot') {{
        ctx.fillStyle = '#37474f'; ctx.fillRect(-12, -38, 24, 32);
    }}
    ctx.restore();
}}

function gameLoop() {{
    if (gamePhase === 'DRESSING_ROOM' || gamePhase === 'EXPLORE') {{
        let moveX = 0;
        if (keys.left) moveX = -speed;
        if (keys.right) moveX = speed;

        if (activeChar === 'trio') {{ yattaPos.vx = moveX; looeyPos.vx = moveX; blotPos.vx = moveX; }}
        else if (activeChar === 'yatta') {{ yattaPos.vx = moveX; looeyPos.vx = 0; blotPos.vx = 0; }}
        else if (activeChar === 'looey') {{ yattaPos.vx = 0; looeyPos.vx = moveX; blotPos.vx = 0; }}
        else if (activeChar === 'blot') {{ yattaPos.vx = 0; looeyPos.vx = 0; blotPos.vx = moveX; }}

        [yattaPos, looeyPos, blotPos].forEach(p => {{
            p.vy += 0.4; p.x += p.vx; p.y += p.vy;
            if (p.y >= 450) {{ p.y = 450; p.vy = 0; p.grounded = true; }}
            if (p.x < 20) p.x = 20; if (p.x > 740) p.x = 740;
        }});
    }}

    ctx.fillStyle = '#06030c'; ctx.fillRect(0, 0, 800, 560);

    if (gamePhase === 'DRESSING_ROOM') {{
        ctx.fillStyle = '#311b92'; ctx.fillRect(60, 300, 70, 150);
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (leadX < 140) {{
            ctx.fillStyle = '#00e676'; ctx.font = '12px Courier New'; ctx.fillText("Interact with door [E]", 45, 285);
        }}
    }}

    ctx.fillStyle = '#281145'; ctx.fillRect(0, 450, 800, 110);
    ctx.fillStyle = '#7c4dff'; ctx.fillRect(0, 450, 800, 4);

    drawPixelCharacter(yattaPos.x, yattaPos.y, 'yatta');
    drawPixelCharacter(looeyPos.x, looeyPos.y, 'looey');
    drawPixelCharacter(blotPos.x, blotPos.y, 'blot');

    requestAnimationFrame(gameLoop);
}}

updateDialogue();
gameLoop();
</script>
</body>
</html>
"""

components.html(game_code, height=620)
