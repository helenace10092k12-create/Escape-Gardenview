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

game_code = r"""
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
            height: 580px;
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
            height: 380px;
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

        #dialogue-area {
            height: 160px;
            background: #080312;
            border-top: 3px solid #512da8;
            padding: 12px 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }
        #speaker { color: #ffb74d; font-weight: bold; font-size: 13px; margin-bottom: 4px; }
        #dialogue-text { color: #00e676; font-size: 12px; line-height: 1.4; height: 60px; }
        
        .dialogue-btns {
            display: flex;
            gap: 10px;
        }
        .action-btn {
            background: #311b92; color: #ede7f6; border: 1px solid #7c4dff;
            padding: 4px 10px; font-size: 11px; cursor: pointer; border-radius: 4px;
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
                <button class="toon-btn active" id="btn-yatta" onclick="switchCharacter('yatta')">[1] Yatta</button>
                <button class="toon-btn" id="btn-looey" onclick="switchCharacter('looey')">[2] Looey</button>
                <button class="toon-btn" id="btn-blot" onclick="switchCharacter('blot')">[3] Blot</button>
                <button class="toon-btn" id="btn-trio" onclick="switchCharacter('trio')">[4] Trio</button>
            </div>
            <button class="lang-btn" id="lang-btn" onclick="toggleLanguage()">VIE / ENG</button>
        </div>
    </div>

    <div id="canvas-holder">
        <canvas id="gameCanvas" width="800" height="380"></canvas>
        <div id="crt-overlay"></div>
        <div id="info-popup">
            <div id="info-title">CHARACTER INFO</div>
            <div id="info-desc">Description here...</div>
        </div>
    </div>

    <div id="dialogue-area">
        <div>
            <div id="speaker">NARRATOR</div>
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
let activeChar = 'yatta';
let popupTimer = null;
let gamePhase = 'DRESSING_ROOM'; // DRESSING_ROOM, BLACKOUT, BUTTON_PHASE, PORTAL_ANIM, GARDENVIEW_SPIT, EXPLORE

let player = {
    x: 360, y: 245, w: 40, h: 56,
    vx: 0, vy: 0, speed: 3.5, jumpPower: -9,
    grounded: false, facing: 'right'
};

let redButton = { x: 0, y: 290, active: false };
let animTimer = 0;
let portalAnimProgress = 0;

const keys = { left: false, right: false };

window.addEventListener('keydown', (e) => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    
    if (e.code === 'KeyW' || e.code === 'ArrowUp') {
        if (player.grounded && gamePhase !== 'PORTAL_ANIM') {
            player.vy = player.jumpPower;
            player.grounded = false;
        }
    }
    
    if (e.code === 'Space') {
        if (gamePhase === 'DRESSING_ROOM' && currentStep !== 4 && currentStep !== 7) {
            nextLine();
        } else if (gamePhase === 'BLACKOUT' && currentStep !== 6) {
            nextLine();
        } else if (gamePhase === 'GARDENVIEW_SPIT') {
            nextLine();
        }
    }

    if (e.code === 'Digit1') switchCharacter('yatta');
    if (e.code === 'Digit2') switchCharacter('looey');
    if (e.code === 'Digit3') switchCharacter('blot');
    if (e.code === 'Digit4') switchCharacter('trio');

    // Phím [E] tương tác
    if (e.code === 'KeyE') {
        if (gamePhase === 'DRESSING_ROOM' && currentStep === 4 && player.x < 140) {
            gamePhase = 'BLACKOUT';
            currentStep = 5; // Rầm! Đèn tắt
            updateDialogue();
        } else if (gamePhase === 'BUTTON_PHASE' && redButton.active && Math.abs(player.x - redButton.x) < 40) {
            redButton.active = false;
            gamePhase = 'PORTAL_ANIM';
            portalAnimProgress = 0;
            currentStep = 9; // Cổng ảo mở ra hút vào
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
        blot: { name: "BLOT (Mime & Clone)", desc: "Completely silent, capable of creating clones to trick monsters." },
        trio: { name: "CIRCUS TRIO", desc: "The united power of all three members to survive in Gardenview!" }
    },
    VIE: {
        yatta: { name: "YATTA (Dẻo dai)", desc: "Linh hoạt, chuyên leo trèo các khu vực cao." },
        looey: { name: "LOOEY (Chạy nhanh)", desc: "Chạy cực nhanh để né tránh các Twisted bám đuổi." },
        blot: { name: "BLOT (Hề câm & Tạo clone)", desc: "Im lặng tuyệt đối, có khả năng tạo phân thân đánh lừa quái." },
        trio: { name: "CIRCUS TRIO", desc: "Sức mạnh đoàn kết cả ba thành viên để sinh tồn trong Gardenview!" }
    }
};

const introScript = {
    ENG: [
        { speaker: "NARRATOR", text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to the dressing room to rest after the thunderous applause." },
        { speaker: "YATTA", text: "Whew... that was a blast today! The Toon crowd was so energetic." },
        { speaker: "LOOEY", text: "My balloons almost popped right at the finale! Haha!" },
        { speaker: "BLOT", text: "...tiaW !enoom eht fo renroc eht ni yltneg gnīmilms ,yltnelis sdoN (Nods silently, smiling gently in the corner of the room.)" },
        { speaker: "SYSTEM", text: "Interact with the door: Move near the dressing room door and press [E]." },
        // [Index 5]
        { speaker: "NARRATOR", text: "SLAM! Suddenly, the heavy iron door of the dressing room automatically slams shut and locks tight!" },
        { speaker: "BLOT", text: "!tuocaolb latoT !tuo tew sthgih eht... edah nawoK (Wait... The lights went out! Total blackout?!)" },
        // [Index 7]
        { speaker: "YATTA", text: "Huh... what is that glowing red button right under us? A strange red button..." },
        { speaker: "SYSTEM", text: "Interact with the red button: Walk to it and press [E]." },
        // [Index 9]
        { speaker: "NARRATOR", text: "WHOOSH! A swirling virtual portal opens wide! The trio desperately grabs onto furniture, swirling and getting sucked in..." },
        { speaker: "NARRATOR", text: "...And finally, they are spit out from the top-left portal into a cold, desolate place. Is this Gardenview? No... it's rundown and eerie!" },
        { speaker: "SYSTEM", text: "WELCOME TO GARDENVIEW ESCAPE GAME. COLLECT 8 GOLDEN KEYS TO FORM THE PUMPKIN KEY AND ESCAPE!" },
        { speaker: "SYSTEM", text: "Controls: [A/D] Move, [W/Up] Jump, [Space] Next Dialogue, [E] Interact, [Z] Skill, [1-4] Switch Toon." }
    ],
    VIE: [
        { speaker: "DẪN CHUYỆN", text: "Buổi biểu diễn trước các Toon vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ để nghỉ ngơi sau tiếng vỗ tay vang dội." },
        { speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê luôn." },
        { speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", text: "...moorp eht fo renroc eht ni yltneg gnīmilms ,yltnelis sdoN (Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng)" },
        { speaker: "HỆ THỐNG", text: "Interact with the door: Di chuyển lại gần cửa phòng thay đồ và bấm [E]." },
        // [Index 5]
        { speaker: "DẪN CHUYỆN", text: "RẦM! Đột nhiên, cánh cửa sắt phòng thay đồ tự động sập đóng lại chặt cứng!" },
        { speaker: "BLOT", text: "!?tuocaolb latoT !tuo tew sthgih ehT ...ad ah nawoK (Khoan đã... Đèn tắt hết rồi! Blackout toàn tập?!)" },
        // [Index 7]
        { speaker: "YATTA", text: "Ơ kìa... cái gì đang phát sáng ngay dưới chân tụi mình thế kia? Một cái nút đỏ kỳ lạ..." },
        { speaker: "HỆ THỐNG", text: "Interact with the red button: Di chuyển đến chỗ cái nút và bấm [E]." },
        // [Index 9]
        { speaker: "DẪN CHUYỆN", text: "VÉO VÉO! Một cánh cổng ảo xoáy sâu mở ra! Cả ba bám chặt vào đồ đạc, xoay vòng tròn rồi bị hút tuột vào trong..." },
        { speaker: "DẪN CHUYỆN", text: "...Và rồi, cổng ở góc trái nhả phăng cả nhóm xuống đất lạnh lẽo. Gardenview đây sao? Không... nó tồi tàn và âm u đến rợn ngáy!" },
        { speaker: "HỆ THỐNG", text: "CHÀO MỪNG ĐẾN VỚI TRÒ CHƠI TRỐN THOÁT. THU THẬP 8 CHÌA KHÓA VÀNG ĐỂ HỢP THỂ THÀNH CHÌA KHÓA BÍ NGÔ!" },
        { speaker: "HỆ THỐNG", text: "Điều khiển: [A/D] Di chuyển, [W/Up] Nhảy, [Space] Tiếp theo, [E] Tương tác, [Z] Kỹ năng, [1-4] Đổi nhân vật." }
    ]
};

function toggleLanguage() {
    currentLang = currentLang === 'ENG' ? 'VIE' : 'ENG';
    document.getElementById('lang-btn').innerText = currentLang === 'ENG' ? 'VIE / ENG' : 'ENG / VIE';
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
    if (gamePhase === 'DRESSING_ROOM' && currentStep === 4) return; // Chờ bấm E cửa
    if (gamePhase === 'BUTTON_PHASE' && currentStep === 8) return;  // Chờ bấm E nút đỏ
    if (gamePhase === 'PORTAL_ANIM') return;                      // Đang chạy animation hút

    currentStep++;
    const maxSteps = introScript[currentLang].length;
    if (currentStep >= maxSteps) {
        currentStep = maxSteps - 1;
    }

    // Kích hoạt trạng thái chờ tương tác cửa
    if (currentStep === 4) {
        gamePhase = 'DRESSING_ROOM';
    }
    // Kích hoạt xuất hiện nút đỏ ngay tại chỗ đứng của nhân vật
    else if (currentStep === 7) {
        gamePhase = 'BUTTON_PHASE';
        redButton.x = player.x + 10; // Xuất hiện ngay dưới chân / cạnh nhân vật
        redButton.active = true;
    }
    // Khi đến đoạn nhả ra ở Gardenview
    else if (currentStep === 10) {
        gamePhase = 'EXPLORE';
        player.x = 120; // Nhả ra từ góc trái
        player.y = 250;
    }

    updateDialogue();
}

function updateDialogue() {
    const data = introScript[currentLang][currentStep];
    document.getElementById('speaker').innerText = data.speaker;
    document.getElementById('dialogue-text').innerText = data.text;
    
    if (gamePhase === 'DRESSING_ROOM' && currentStep === 4) {
        document.getElementById('next-btn').innerText = currentLang === 'ENG' ? "[Interact with Door (Press E)]" : "[Interact with Door (Bấm E)]";
    } else if (gamePhase === 'BUTTON_PHASE' && currentStep === 8) {
        document.getElementById('next-btn').innerText = currentLang === 'ENG' ? "[Interact with Red Button (Press E)]" : "[Interact with Red Button (Bấm E)]";
    } else {
        document.getElementById('next-btn').innerText = currentLang === 'ENG' ? "Next [Space] >" : "Tiếp theo [Space] >";
    }
}

function drawPixelCharacter(x, y, type, angle = 0, scale = 1) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.scale(scale, scale);

    if (type === 'yatta') {
        ctx.fillStyle = '#fff59d';
        ctx.fillRect(-12, -28, 24, 22);
        ctx.fillStyle = '#ff80ab';
        ctx.fillRect(-16, -38, 8, 12);
        ctx.fillRect(8, -38, 8, 12);
        ctx.fillStyle = '#4fc3f7';
        ctx.fillRect(-14, -36, 4, 5);
        ctx.fillRect(10, -36, 4, 5);
        ctx.fillStyle = '#4fc3f7';
        ctx.fillRect(-10, -24, 20, 14);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-9, -23, 6, 8);
        ctx.fillStyle = '#111111';
        ctx.fillRect(-7, -20, 3, 4);

        ctx.fillStyle = '#ff80ab';
        ctx.fillRect(-12, -6, 24, 18);
    } 
    else if (type === 'looey') {
        ctx.fillStyle = '#ffee58';
        ctx.fillRect(-14, -26, 28, 24);
        ctx.fillStyle = '#66bb6a';
        ctx.fillRect(-10, -44, 8, 18);
        ctx.fillStyle = '#ab47bc';
        ctx.fillRect(2, -44, 8, 18);
        ctx.fillStyle = '#ff7043';
        ctx.fillRect(-12, -2, 24, 18);
    } 
    else if (type === 'blot') {
        ctx.fillStyle = '#37474f';
        ctx.fillRect(-12, -28, 24, 26);
        ctx.fillStyle = '#212121';
        ctx.fillRect(-12, -28, 14, 16);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(2, -22, 8, 8);
        ctx.fillStyle = '#000000';
        ctx.fillRect(5, -20, 3, 3);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-12, -2, 24, 18);
    }
    ctx.restore();
}

function gameLoop() {
    // Xử lý vật lý di chuyển khi không chạy animation hút
    if (gamePhase !== 'PORTAL_ANIM' && gamePhase !== 'GARDENVIEW_SPIT') {
        if (keys.left) { player.vx = -player.speed; player.facing = 'left'; }
        else if (keys.right) { player.vx = player.speed; player.facing = 'right'; }
        else { player.vx = 0; }

        player.vy += 0.4;
        player.x += player.vx;
        player.y += player.vy;

        if (player.y >= 250) {
            player.y = 250;
            player.vy = 0;
            player.grounded = true;
        }

        if (player.x < 20) player.x = 20;
        if (player.x > 740) player.x = 740;
    }

    // --- RENDER BACKGROUND & GRAPHICS ---
    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#030103' : '#06030c'; // Gardenview âm u hơn
    ctx.fillRect(0, 0, 800, 380);

    // Gạch nền ô vuông FNAF retro
    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#0a030f' : '#0f071a';
    for(let x = 0; x < 800; x += 40) {
        for(let y = 0; y < 380; y += 40) {
            if ((x/40 + y/40) % 2 === 0) ctx.fillRect(x, y, 40, 40);
        }
    }

    // 1. Cửa phòng thay đồ (Chỉ hiện ở pha đầu)
    if (gamePhase === 'DRESSING_ROOM' || gamePhase === 'BLACKOUT' || gamePhase === 'BUTTON_PHASE') {
        ctx.fillStyle = '#311b92';
        ctx.fillRect(60, 150, 70, 156);
        ctx.strokeStyle = '#7c4dff';
        ctx.lineWidth = 3;
        ctx.strokeRect(60, 150, 70, 156);
        ctx.fillStyle = '#ffb74d';
        ctx.fillRect(115, 230, 6, 10);

        if (currentStep === 4 && player.x < 140) {
            ctx.fillStyle = '#00e676';
            ctx.font = '11px Courier New';
            ctx.fillText("Interact with door [E]", 50, 140);
        }
    }

    // 2. Nút bấm màu đỏ xuất hiện ngay chỗ nhân vật đứng
    if (gamePhase === 'BUTTON_PHASE' && redButton.active) {
        ctx.fillStyle = '#d50000';
        ctx.fillRect(redButton.x, 292, 24, 12);
        ctx.fillStyle = '#ff1744';
        ctx.fillRect(redButton.x + 4, 288, 16, 6);

        if (Math.abs(player.x - redButton.x) < 40) {
            ctx.fillStyle = '#00e676';
            ctx.font = '11px Courier New';
            ctx.fillText("Interact with Red Button [E]", redButton.x - 40, 275);
        }
    }

    // 3. Animation hút vào cổng
    if (gamePhase === 'PORTAL_ANIM') {
        portalAnimProgress += 0.05;
        let rot = portalAnimProgress * 10;
        let scale = Math.max(0.1, 1 - portalAnimProgress * 0.3);
        
        // Vẽ tâm hút ở giữa màn hình
        ctx.fillStyle = '#ff1744';
        ctx.beginPath();
        ctx.arc(400, 250, Math.min(100, portalAnimProgress * 40), 0, Math.PI * 2);
        ctx.fill();

        drawPixelCharacter(400 + Math.sin(rot)*30, 250 + Math.cos(rot)*30, activeChar, rot, scale);

        if (portalAnimProgress > 3) {
            gamePhase = 'GARDENVIEW_SPIT';
            currentStep = 10; // Chuyển cảnh nhả ra ở Gardenview
            updateDialogue();
        }
    }

    // 4. Cổng Gardenview ở góc trái nhả nhóm ra (Nằm dưới đất rồi đứng dậy)
    if (gamePhase === 'GARDENVIEW_SPIT' || gamePhase === 'EXPLORE') {
        // Cổng ở góc trái (x: 100, y: 220)
        ctx.fillStyle = '#00e676';
        ctx.beginPath();
        ctx.ellipse(100, 230, 30, 45, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
    }

    // Sàn nhà
    ctx.fillStyle = gamePhase === 'EXPLORE' ? '#180824' : '#281145';
    ctx.fillRect(0, 306, 800, 74);
    ctx.fillStyle = '#7c4dff';
    ctx.fillRect(0, 306, 800, 4);

    // Vẽ nhân vật (Nếu không ở pha portal anim)
    if (gamePhase !== 'PORTAL_ANIM') {
        if (activeChar === 'yatta') {
            drawPixelCharacter(player.x, player.y - 25, 'yatta');
        } else if (activeChar === 'looey') {
            drawPixelCharacter(player.x, player.y - 25, 'looey');
        } else if (activeChar === 'blot') {
            drawPixelCharacter(player.x, player.y - 25, 'blot');
        } else {
            drawPixelCharacter(player.x - 40, player.y - 25, 'yatta');
            drawPixelCharacter(player.x, player.y - 25, 'looey');
            drawPixelCharacter(player.x + 40, player.y - 25, 'blot');
        }
    }

    requestAnimationFrame(gameLoop);
}

updateDialogue();
showCharPopup('yatta');
gameLoop();
</script>
</body>
</html>
"""

components.html(game_code, height=620)
