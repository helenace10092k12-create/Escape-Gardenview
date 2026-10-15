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
<html lang="vi">
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
                <button class="toon-btn" id="btn-yatta" onclick="switchCharacter('yatta')">[1] Yatta</button>
                <button class="toon-btn" id="btn-looey" onclick="switchCharacter('looey')">[2] Looey</button>
                <button class="toon-btn" id="btn-blot" onclick="switchCharacter('blot')">[3] Blot</button>
                <button class="toon-btn active" id="btn-trio" onclick="switchCharacter('trio')">[4] Trio</button>
            </div>
            <button class="lang-btn" id="lang-btn" onclick="toggleLanguage()">VIE / ENG</button>
        </div>
    </div>

    <div id="canvas-holder">
        <canvas id="gameCanvas" width="800" height="380"></canvas>
        <div id="crt-overlay"></div>
        <div id="info-popup">
            <div id="info-title">THÔNG TIN NHÂN VẬT</div>
            <div id="info-desc">Mô tả ở đây...</div>
        </div>
    </div>

    <div id="dialogue-area">
        <div>
            <div id="speaker">DẪN CHUYỆN</div>
            <div id="dialogue-text">Đang tải phần mở đầu...</div>
        </div>
        <div class="dialogue-btns">
            <button class="action-btn" id="next-btn" onclick="nextLine()">Tiếp theo [Space] ></button>
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let currentLang = 'VIE'; // Mặc định Tiếng Việt cho đúng yêu cầu
let currentStep = 0;
let activeChar = 'trio'; // Mặc định điều khiển cả 3 đứa (Trio)
let popupTimer = null;
let gamePhase = 'DRESSING_ROOM'; 

// Vị trí độc lập của từng thành viên trong Circus Trio
let yattaPos = { x: 320, y: 306, vx: 0, vy: 0, grounded: true };
let looeyPos = { x: 360, y: 306, vx: 0, vy: 0, grounded: true };
let blotPos  = { x: 400, y: 306, vx: 0, vy: 0, grounded: true };

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

const charInfoData = {
    VIE: {
        yatta: { name: "YATTA (Dẻo dai)", desc: "Linh hoạt, chuyên leo trèo các khu vực cao trong Gardenview." },
        looey: { name: "LOOEY (Chạy nhanh)", desc: "Chạy cực nhanh để né tránh các Twisted bám đuổi sát nút." },
        blot: { name: "BLOT (Hề câm & Tạo bản sao)", desc: "Im lặng tuyệt đối, có khả năng tạo phân thân đánh lừa quái." },
        trio: { name: "CIRCUS TRIO", desc: "Sức mạnh đoàn kết của cả ba thành viên để sinh tồn!" }
    },
    ENG: {
        yatta: { name: "YATTA (Acrobatic)", desc: "Flexible, agile, specialized in climbing high areas." },
        looey: { name: "LOOEY (Fast Runner)", desc: "Runs extremely fast to escape pursuing Twisted toons." },
        blot: { name: "BLOT (Mime & Clone)", desc: "Completely silent, capable of creating clones to trick monsters." },
        trio: { name: "CIRCUS TRIO", desc: "The united power of all three members to survive in Gardenview!" }
    }
};

const introScript = {
    VIE: [
        { speaker: "DẪN CHUYỆN", text: "Buổi biểu diễn trước các Toon vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ để nghỉ ngơi sau tiếng vỗ tay vang dội." },
        { speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê luôn." },
        { speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", text: "...moorp eht fo renroc eht ni yltneg gnīmilms ,yltnelis sdoN (Dịch: Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng)." },
        { speaker: "HỆ THỐNG", text: "Nhiệm vụ: Di chuyển lại gần cánh cửa phòng thay đồ và nhấn [E] để tương tác." },
        { speaker: "DẪN CHUYỆN", text: "RẦM! Đột nhiên, cánh cửa sắt phòng thay đồ tự động sập đóng lại chặt cứng!" },
        { speaker: "BLOT", text: "!?tuocaolb latoT !tuo tew sthgih ehT ...ad ah nawoK (Dịch: Khoan đã... Đèn tắt hết rồi! Mất điện toàn tập rồi sao?!)" },
        { speaker: "YATTA", text: "Ơ kìa... cái gì đang phát sáng đỏ rực ngay dưới chân tụi mình thế kia? Một cái nút bấm kỳ lạ..." },
        { speaker: "HỆ THỐNG", text: "Nhiệm vụ: Di chuyển đến sát cái nút bấm và nhấn [E] để tương tác." },
        { speaker: "DẪN CHUYỆN", text: "VÉO VÉO! Một cánh cổng ảo xoáy sâu mở ra! Cả ba bám chặt vào đồ đạc, xoay vòng tròn rồi bị hút tuột vào trong..." },
        { speaker: "DẪN CHUYỆN", text: "...Và rồi, cổng ở góc trái nhả phăng cả nhóm xuống đất lạnh lẽo. Gardenview đây sao? Không... nó tồi tàn và âm u đến rợn ngáy!" },
        { speaker: "HỆ THỐNG", text: "CHÀO MỪNG ĐẾN TRÒ CHƠI TRỐN THOÁT. THU THẬP 8 CHÌA KHÓA VÀNG ĐỂ HỢP THỂ THÀNH CHÌA KHÓA BÍ NGÔ!" },
        { speaker: "HỆ THỐNG", text: "Điều khiển: [A/D] Di chuyển, [W/Up] Nhảy, [Space] Tiếp theo, [E] Tương tác, [1-4] Đổi nhân vật." }
    ],
    ENG: [
        { speaker: "NARRATOR", text: "The show for the Toons has just concluded successfully. The Circus Trio heads back to the dressing room to rest after the thunderous applause." },
        { speaker: "YATTA", text: "Whew... that was a blast today! The Toon crowd was so energetic." },
        { speaker: "LOOEY", text: "My balloons almost popped right at the finale! Haha!" },
        { speaker: "BLOT", text: "...tiaW !enoom eht fo renroc eht ni yltneg gnīmilms ,yltnelis sdoN (Trans: Nods silently, smiling gently in the corner of the room)." },
        { speaker: "SYSTEM", text: "Interact with the door: Move near the dressing room door and press [E]." },
        { speaker: "NARRATOR", text: "SLAM! Suddenly, the heavy iron door of the dressing room automatically slams shut and locks tight!" },
        { speaker: "BLOT", text: "!tuocaolb latoT !tuo tew sthgih eht... edah nawoK (Trans: Wait... The lights went out! Total blackout?!)" },
        { speaker: "YATTA", text: "Huh... what is that glowing red button right under us? A strange red button..." },
        { speaker: "SYSTEM", text: "Interact with the red button: Walk to it and press [E]." },
        { speaker: "NARRATOR", text: "WHOOSH! A swirling virtual portal opens wide! The trio desperately grabs onto furniture, swirling and getting sucked in..." },
        { speaker: "NARRATOR", text: "...And finally, they are spit out from the top-left portal into a cold, desolate place. Is this Gardenview? No... it's rundown and eerie!" },
        { speaker: "SYSTEM", text: "WELCOME TO GARDENVIEW ESCAPE GAME. COLLECT 8 GOLDEN KEYS TO FORM THE PUMPKIN KEY AND ESCAPE!" },
        { speaker: "SYSTEM", text: "Controls: [A/D] Move, [W/Up] Jump, [Space] Next Dialogue, [E] Interact, [1-4] Switch Toon." }
    ]
};

function toggleLanguage() {
    currentLang = currentLang === 'VIE' ? 'ENG' : 'VIE';
    document.getElementById('lang-btn').innerText = currentLang === 'VIE' ? 'VIE / ENG' : 'ENG / VIE';
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
    if (gamePhase === 'DRESSING_ROOM' && currentStep === 4) return;
    if (gamePhase === 'BUTTON_PHASE' && currentStep === 8) return;
    if (gamePhase === 'PORTAL_ANIM') return;

    currentStep++;
    const maxSteps = introScript[currentLang].length;
    if (currentStep >= maxSteps) {
        currentStep = maxSteps - 1;
    }

    if (currentStep === 4) {
        gamePhase = 'DRESSING_ROOM';
    } else if (currentStep === 7) {
        gamePhase = 'BUTTON_PHASE';
        let leadX = activeChar === 'yatta' ? yattaPos.x : activeChar === 'looey' ? looeyPos.x : activeChar === 'blot' ? blotPos.x : yattaPos.x;
        redButton.x = leadX + 10;
        redButton.active = true;
    } else if (currentStep === 10) {
        gamePhase = 'EXPLORE';
        yattaPos.x = 100; yattaPos.y = 306;
        looeyPos.x = 135; looeyPos.y = 306;
        blotPos.x  = 170; blotPos.y  = 306;
    }

    updateDialogue();
}

function updateDialogue() {
    const data = introScript[currentLang][currentStep];
    document.getElementById('speaker').innerText = data.speaker;
    document.getElementById('dialogue-text').innerText = data.text;
    
    if (gamePhase === 'DRESSING_ROOM' && currentStep === 4) {
        document.getElementById('next-btn').innerText = currentLang === 'VIE' ? "[Interact with Door (Bấm E)]" : "[Interact with Door (Press E)]";
    } else if (gamePhase === 'BUTTON_PHASE' && currentStep === 8) {
        document.getElementById('next-btn').innerText = currentLang === 'VIE' ? "[Interact with Red Button (Bấm E)]" : "[Interact with Red Button (Press E)]";
    } else {
        document.getElementById('next-btn').innerText = currentLang === 'VIE' ? "Tiếp theo [Space] >" : "Next [Space] >";
    }
}

// Vẽ Pixel Art nhân vật Yatta, Looey, Blot chuẩn chỉnh
function drawPixelCharacter(x, y, type, angle = 0, scale = 1, isSelected = false) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.scale(scale
