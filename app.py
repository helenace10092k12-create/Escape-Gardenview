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

        #info-popup {
            position: absolute; top: 50px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 5, 30, 0.95); border: 2px solid #00e676;
            padding: 8px 16px; border-radius: 6px; text-align: center; z-index: 30; display: none;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.5);
        }
        #info-title { color: #00e676; font-size: 12px; font-weight: bold; margin-bottom: 2px; }
        #info-desc { color: #e0f2f1; font-size: 10px; }

        /* KHUNG CHAT CHỈ HIỆN KHI CÓ HỘI THOẠI / DẪN CHUYỆN */
        #dialogue-area {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 800px;
            height: 200px;
            background: #080312;
            border-top: 3px solid #512da8;
            padding: 12px 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            z-index: 40;
            box-shadow: 0 -5px 25px rgba(81, 45, 168, 0.5);
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
            display: none; /* Mặc định ẩn, chỉ hiện khi nhân vật cụ thể nói */
        }
        #portrait-box img { width: 100%; height: 100%; object-fit: cover; image-rendering: pixelated; }

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
        .dialogue-btns { display: flex; justify-content: flex-end; gap: 10px; }
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
        <canvas id="gameCanvas" width="800" height="560"></canvas>
        <div id="crt-overlay"></div>
        <div id="info-popup">
            <div id="info-title">CHARACTER INFO</div>
            <div id="info-desc">Description here...</div>
        </div>
    </div>

    <!-- KHUNG CHAT TỰ ĐỘNG BẬT/TẮT THEO NGỮ CẢNH -->
    <div id="dialogue-area">
        <div id="portrait-box">
            <img id="portrait-img" src="" alt="Character Portrait">
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
let gamePhase = 'INTRO_DIALOGUE'; // Bắt đầu bằng hội thoại giới thiệu

let yattaPos = { x: 320, y: 450, vx: 0, vy: 0, grounded: true };
let looeyPos = { x: 360, y: 450, vx: 0, vy: 0, grounded: true };
let blotPos  = { x: 400, y: 450, vx: 0, vy: 0, grounded: true };

let speed = 3.5;
let jumpPower = -9;
let redButton = { x: 0, active: false };
let portalAnimProgress = 0;

const keys = { left: false, right: false };

window.addEventListener('keydown', (e) => {
    // Nếu đang trong hội thoại thì chặn di chuyển nhân vật bên dưới
    if (gamePhase === 'INTRO_DIALOGUE' || gamePhase === 'BLACKOUT_TALK') {
        if (e.code === 'Space') nextLine();
        return;
    }

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
        nextLine();
    }

    if (e.code === 'Digit1') switchCharacter('yatta');
    if (e.code === 'Digit2') switchCharacter('looey');
    if (e.code === 'Digit3') switchCharacter('blot');
    if (e.code === 'Digit4') switchCharacter('trio');

    if (e.code === 'KeyE') {
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (gamePhase === 'DRESSING_ROOM' && leadX < 140) {
            gamePhase = 'BLACKOUT_TALK';
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

const charInfoData = {
    ENG: {
        yatta: { name: "YATTA (Acrobatic)", desc: "Flexible, agile, specialized in climbing high areas." },
        looey: { name: "LOOEY (Fast Runner)", desc: "Runs extremely fast to escape pursuing Twisted toons." },
        blot: { name: "BLOT (Mime & Clone)", desc: "Completely silent, capable of creating clones." },
        trio: { name: "CIRCUS TRIO", desc: "The united power of all three members to survive in Gardenview!" }
    },
    VIE: {
        yatta: { name: "YATTA (Dẻo dai)", desc: "Linh hoạt, chuyên leo trèo các khu vực cao." },
        looey: { name: "LOOEY (Chạy nhanh)", desc: "Chạy cực nhanh để né tránh các Twisted." },
        blot: { name: "BLOT (Hề câm & Tạo clone)", desc: "Im lặng tuyệt đối, tạo phân thân đánh lừa quái." },
        trio: { name: "CIRCUS TRIO", desc: "Sức mạnh đoàn kết cả ba thành viên trong Gardenview!" }
    }
};

const introScript = {
    ENG: [
        { speaker: "NARRATOR", type: "system", text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to the dressing room." },
        { speaker: "YATTA", type: "character", img: "YATTA_URL", text: "Whew... that was a blast today! The Toon crowd was so energetic." },
        { speaker: "LOOEY", type: "character", img: "YOUR_IMAGE_URL_HERE", text: "My balloons almost popped right at the finale! Haha!" },
        { speaker: "BLOT", type: "character", img: "BLOT_URL", text: "Nods silently, smiling gently in the corner of the room." },
        { speaker: "SYSTEM", type: "system", text: "Interact with the door: Move near the dressing room door and press [E]." },
        { speaker: "NARRATOR", type: "system", text: "SLAM! Suddenly, the heavy iron door of the dressing room automatically slams shut!" },
        { speaker: "BLOT", type: "character", img: "BLOT_URL", text: "!tuocaolb latoT !tuo tew sthgih eht... edah nawoK (Trans: Wait... The lights went out!)" },
        { speaker: "YATTA", type: "character", img: "YATTA_URL", text: "Huh... what is that glowing red button right under us? A strange red button..." },
        { speaker: "SYSTEM", type: "system", text: "Interact with the red button: Walk to it and press [E]." },
        { speaker: "NARRATOR", type: "system", text: "WHOOSH! A swirling virtual portal opens wide! The trio gets sucked in..." },
        { speaker: "NARRATOR", type: "system", text: "...And finally, they are spit out into a cold, desolate place. Gardenview?" },
        { speaker: "SYSTEM", type: "system", text: "WELCOME TO GARDENVIEW ESCAPE. COLLECT 8 GOLDEN KEYS TO ESCAPE!" }
    ],
    VIE: [
        { speaker: "DẪN CHUYỆN", type: "system", text: "Buổi biểu diễn vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ nghỉ ngơi." },
        { speaker: "YATTA", type: "character", img: "YATTA_URL", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê." },
        { speaker: "LOOEY", type: "character", img: "YOUR_IMAGE_URL_HERE", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", type: "character", img: "BLOT_URL", text: "Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng." },
        { speaker: "HỆ THỐNG", type: "system", text: "Nhiệm vụ: Di chuyển lại gần cửa phòng thay đồ và nhấn [E]." },
        { speaker: "DẪN CHUYỆN", type: "system", text: "RẦM! Cánh cửa sắt phòng thay đồ tự động sập đóng lại chặt cứng!" },
        { speaker: "BLOT", type: "character", img: "BLOT_URL", text: "Khoan đã... Đèn tắt hết rồi! Mất điện toàn tập rồi sao?!" },
        { speaker: "YATTA", type: "character", img: "YATTA_URL", text: "Ơ kìa... cái gì đang phát sáng đỏ rực ngay dưới chân tụi mình thế kia?" },
        { speaker: "HỆ THỐNG", type: "system", text: "Nhiệm vụ: Di chuyển đến sát cái nút bấm và nhấn [E]." },
        { speaker: "DẪN CHUYỆN", type: "system", text: "VÉO VÉO! Một cánh cổng ảo xoáy sâu mở ra rồi hút cả nhóm vào trong..." },
        { speaker: "DẪN CHUYỆN", type: "system", text: "...Và rồi nhóm bị nhả xuống đất lạnh lẽo. Gardenview đây sao? Âm u rợn ngáy!" },
        { speaker: "HỆ THỐNG", type: "system", text: "CHÀO MỪNG ĐẾN TRÒ CHƠI TRỐN THOÁT. THU THẬP 8 CHÌA KHÓA VÀNG!" }
    ]
};

function toggleLanguage() {
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    document.getElementById('lang-btn').innerText = currentLang === 'ENG' ? 'ENG / VIE' : 'VIE / ENG';
    updateDialogue();
    showCharPopup(activeChar);
}

function switchCharacter(char) {
    activeChar = char;
    document.querySelectorAll('.toon-btn').forEach(b => b.classList.remove('active'));
    let btnId = char === 'yatta' ? 'btn-yatta' : char === 'looey' ? 'btn-looey' : char === 'blot' ? 'btn-blot' : 'btn-trio';
    document.getElementById(btnId).classList.add('active');
    showCharPopup(char);
}

function showCharPopup(char) {
    const info = charInfoData[currentLang][char];
    const popup = document.getElementById('info-popup');
    document.getElementById('info-title').innerText = info.name;
    document.getElementById('info-desc').innerText = info.desc;
    popup.style.display = 'block';
    if (popupTimer) clearTimeout(popupTimer);
    popupTimer = setTimeout(() => { popup.style.display = 'none'; }, 10000);
}

function nextLine() {
    const script = introScript[currentLang];
    currentStep++;
    
    if (currentStep >= script.length) {
        // Hết hội thoại mở đầu -> Ẩn khung chat, cho phép người chơi tự do khám phá
        document.getElementById('dialogue-area').style.display = 'none';
        gamePhase = 'EXPLORE';
        return;
    }

    if (currentStep === 4) {
        document.getElementById('dialogue-area').style.display = 'none';
        gamePhase = 'DRESSING_ROOM';
        return;
    }
    if (currentStep === 8) {
        document.getElementById('dialogue-area').style.display = 'none';
        gamePhase = 'BUTTON_PHASE';
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        redButton.x = leadX + 10;
        redButton.active = true;
        return;
    }

    updateDialogue();
}

function updateDialogue() {
    const dialogueArea = document.getElementById('dialogue-area');
    dialogueArea.style.display = 'flex';

    const data = introScript[currentLang][currentStep];
    document.getElementById('speaker-tag').innerText = data.speaker;
    document.getElementById('dialogue-text').innerText = data.text;
    
    const portraitBox = document.getElementById('portrait-box');
    const portraitImg = document.getElementById('portrait-img');

    // CHỈ HIỆN ẢNH KHI LÀ NHÂN VẬT NÓI (CÓ ẢNH RIÊNG)
    if (data.type === 'character' && data.img && data.img !== 'YATTA_URL' && data.img !== 'BLOT_URL') {
        portraitBox.style.display = 'block';
        portraitImg.src = data.img; // Ảnh phác thảo của Looey
    } else {
        portraitBox.style.display = 'none'; // Ẩn khung avatar nếu là Narrator, System hoặc nhân vật khác
    }
}

function drawPixelCharacter(x, y, type, angle = 0, scale = 1, isSelected = false) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.scale(scale, scale);

    if (isSelected && activeChar !== 'trio') {
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(0, -65); ctx.lineTo(-6, -75); ctx.lineTo(6, -75); ctx.closePath();
        ctx.fill();
    }

    if (type === 'yatta') {
        ctx.fillStyle = '#fff59d'; ctx.fillRect(-12, -40, 24, 32);
        ctx.fillStyle = '#ff80ab'; ctx.fillRect(-16, -52, 8, 14); ctx.fillRect(8, -52, 8, 14);
        ctx.fillStyle = '#4fc3f7'; ctx.fillRect(-14, -49, 4, 6); ctx.fillRect(10, -49, 4, 6);
        ctx.fillStyle = '#4fc3f7'; ctx.fillRect(-10, -34, 20, 16);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-9, -32, 6, 8); ctx.fillRect(3, -32, 6, 8);
        ctx.fillStyle = '#111111'; ctx.fillRect(-7, -29, 3, 4); ctx.fillRect(5, -29, 3, 4);
        ctx.fillStyle = '#ff80ab'; ctx.fillRect(-12, -8, 24, 18);
    } else if (type === 'looey') {
        ctx.fillStyle = '#ffee58'; ctx.fillRect(-14, -38, 28, 30);
        ctx.fillStyle = '#66bb6a'; ctx.fillRect(-10, -56, 8, 18);
        ctx.fillStyle = '#ab47bc'; ctx.fillRect(2, -56, 8, 18);
        ctx.fillStyle = '#000000'; ctx.fillRect(-8, -28, 4, 6); ctx.fillRect(4, -28, 4, 6);
        ctx.fillStyle = '#ff7043'; ctx.fillRect(-12, -8, 24, 18);
    } else if (type === 'blot') {
        ctx.fillStyle = '#37474f'; ctx.fillRect(-12, -38, 24, 32);
        ctx.fillStyle = '#212121'; ctx.fillRect(-12, -38, 14, 16);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(2, -30, 8, 8);
        ctx.fillStyle = '#000000'; ctx.fillRect(5, -27, 3, 3);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-12, -8, 24, 18);
    }
    ctx.restore();
}

function gameLoop() {
    if (gamePhase === 'EXPLORE') {
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
            if (p.y >= 450) {
                p.y = 450;
                p.vy = 0;
                p.grounded = true;
            }
            if (p.x < 20) p.x = 20;
            if (p.x > 740) p.x = 740;
        });
    }

    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#030103' : '#06030c';
    ctx.fillRect(0, 0, 800, 560);

    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#0a030f' : '#0f071a';
    for(let x = 0; x < 800; x += 40) {
        for(let y = 0; y < 560; y += 40) {
            if ((x/40 + y/40) % 2 === 0) ctx.fillRect(x, y, 40, 40);
        }
    }

    // Vẽ phòng thay đồ / Cửa
    if (gamePhase === 'DRESSING_ROOM' || gamePhase === 'BLACKOUT_TALK') {
        ctx.fillStyle = '#311b92'; ctx.fillRect(60, 300, 70, 150);
        ctx.strokeStyle = '#7c4dff'; ctx.lineWidth = 3; ctx.strokeRect(60, 300, 70, 150);
        ctx.fillStyle = '#ffb74d'; ctx.fillRect(115, 370, 6, 10);

        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (leadX < 140) {
            ctx.fillStyle = '#00e676'; ctx.font = '12px Courier New'; ctx.fillText("Interact with door [E]", 45, 285);
        }
    }

    if (gamePhase === 'BUTTON_PHASE' && redButton.active) {
        ctx.fillStyle = '#d50000'; ctx.fillRect(redButton.x, 445, 24, 8);
        ctx.fillStyle = '#ff1744'; ctx.fillRect(redButton.x + 4, 441, 16, 4);

        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        if (Math.abs(leadX - redButton.x) < 40) {
            ctx.fillStyle = '#00e676'; ctx.font = '12px Courier New'; ctx.fillText("Interact with Red Button [E]", redButton.x - 40, 425);
        }
    }

    // Sàn nhà
    ctx.fillStyle = '#281145';
    ctx.fillRect(0, 450, 800, 110);
    ctx.fillStyle = '#7c4dff';
    ctx.fillRect(0, 450, 800, 4);

    // Vẽ nhân vật
    drawPixelCharacter(yattaPos.x, yattaPos.y, 'yatta', 0, 1, activeChar === 'yatta');
    drawPixelCharacter(looeyPos.x, looeyPos.y, 'looey', 0, 1, activeChar === 'looey');
    drawPixelCharacter(blotPos.x, blotPos.y, 'blot', 0, 1, activeChar === 'blot');

    requestAnimationFrame(gameLoop);
}

updateDialogue();
showCharPopup('trio');
gameLoop();
</script>
</body>
</html>
"""

components.html(game_code, height=620)
