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

let player = {
    x: 100, y: 270, w: 24, h: 50,
    vx: 0, vy: 0, speed: 3.5, jumpPower: -9,
    grounded: false, facing: 'right'
};

const keys = { left: false, right: false };

window.addEventListener('keydown', (e) => {
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
    if (e.code === 'KeyW' || e.code === 'Space' || e.code === 'ArrowUp') {
        if (player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
        }
    }
    if (e.code === 'Digit1') switchCharacter('yatta');
    if (e.code === 'Digit2') switchCharacter('looey');
    if (e.code === 'Digit3') switchCharacter('blot');
    if (e.code === 'Digit4') switchCharacter('trio');

    if (e.code === 'KeyE') {
        console.log("Interacted with [E]");
    }
    if (e.code === 'KeyZ') {
        console.log("Used Skill / Weapon with [Z]");
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
        { speaker: "BLOT", text: "(Nods silently, smiling gently in the corner of the room)." },
        { speaker: "NARRATOR", text: "*SLAM!* Suddenly, the heavy iron door of the dressing room automatically slams shut and locks tight!" },
        { speaker: "BLOT", text: "Wait... The lights went out! Total blackout?!" },
        { speaker: "YATTA", text: "Huh... what is that glowing thing right in the middle of the floor? A strange red button..." },
        { speaker: "NARRATOR", text: "Out of curiosity, Yatta steps forward and accidentally touches the button..." },
        { speaker: "NARRATOR", text: "*WHOOSH!* A swirling virtual portal opens wide! The trio desperately grabs onto furniture, but the suction is too strong..." },
        { speaker: "NARRATOR", text: "...And finally, they are spit out into a cold, desolate place. Is this Gardenview? No... it's rundown and eerily gloomy!" },
        { speaker: "SYSTEM", text: "WELCOME TO GARDENVIEW ESCAPE GAME. COLLECT 8 GOLDEN KEYS TO FORM THE PUMPKIN KEY AND ESCAPE!" },
        { speaker: "SYSTEM", text: "Controls: [A/D] Move, [W/Space] Jump, [E] Interact, [Z] Skill/Weapon, [1-4] Switch Character." }
    ],
    VIE: [
        { speaker: "DẪN CHUYỆN", text: "Buổi biểu diễn trước các Toon vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ để nghỉ ngơi sau tiếng vỗ tay vang dội." },
        { speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê luôn." },
        { speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
        { speaker: "BLOT", text: "(Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng)." },
        { speaker: "DẪN CHUYỆN", text: "*RẦM!* Đột nhiên, cánh cửa sắt phòng thay đồ tự động sập đóng lại chặt cứng!" },
        { speaker: "BLOT", text: "Khoan đã... Đèn tắt hết rồi! Blackout toàn tập?!" },
        { speaker: "YATTA", text: "Ơ kìa... cái gì đang phát sáng ở giữa sàn nhà thế kia? Một cái nút màu đỏ kỳ lạ..." },
        { speaker: "DẪN CHUYỆN", text: "Vì tò mò, Yatta bước đến và vô tình chạm vào nút bấm..." },
        { speaker: "DẪN CHUYỆN", text: "*VÉO VÉO!* Một cánh cổng ảo xoáy sâu mở ra! Cả ba hốt hoảng bám chặt vào đồ đạc nhưng lực hút quá mạnh..." },
        { speaker: "DẪN CHUYỆN", text: "...Và rồi, cả nhóm bị 'nhả' phăng xuống một nơi lạnh lẽo. Gardenview đây sao? Không... nó tồi tàn và âm u đến rợn ngáy!" },
        { speaker: "HỆ THỐNG", text: "CHÀO MỪNG ĐẾN VỚI TRÒ CHƠI TRỐN THOÁT. THU THẬP 8 CHÌA KHÓA VÀNG ĐỂ HỢP THỂ THÀNH CHÌA KHÓA BÍ NGÔ!" },
        { speaker: "HỆ THỐNG", text: "Điều khiển: [A/D] Di chuyển, [W/Space] Nhảy, [E] Tương tác, [Z] Kỹ năng/Vũ khí, [1-4] Đổi nhân vật." }
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
    popupTimer = setTimeout(() => {
        popup.style.display = 'none';
    }, 10000);
}

function nextLine() {
    currentStep++;
    const maxSteps = introScript[currentLang].length;
    if (currentStep >= maxSteps) {
        currentStep = maxSteps - 1;
    }
    updateDialogue();
}

function updateDialogue() {
    const data = introScript[currentLang][currentStep];
    document.getElementById('speaker').innerText = data.speaker;
    document.getElementById('dialogue-text').innerText = data.text;
    document.getElementById('next-btn').innerText = currentLang === 'ENG' ? "Next [Space] >" : "Tiếp theo [Space] >";
}

function gameLoop() {
    if (keys.left) { player.vx = -player.speed; player.facing = 'left'; }
    else if (keys.right) { player.vx = player.speed; player.facing = 'right'; }
    else { player.vx = 0; }

    player.vy += 0.4;
    player.x += player.vx;
    player.y += player.vy;

    if (player.y >= 270) {
        player.y = 270;
        player.vy = 0;
        player.grounded = true;
    }

    if (player.x < 20) player.x = 20;
    if (player.x > 750) player.x = 750;

    ctx.fillStyle = '#06030c';
    ctx.fillRect(0, 0, 800, 380);

    ctx.fillStyle = '#0f071a';
    for(let x = 0; x < 800; x += 40) {
        for(let y = 0; y < 380; y += 40) {
            if ((x/40 + y/40) % 2 === 0) ctx.fillRect(x, y, 40, 40);
        }
    }

    ctx.fillStyle = '#281145';
    ctx.fillRect(0, 320, 800, 60);
    ctx.fillStyle = '#7c4dff';
    ctx.fillRect(0, 320, 800, 4);

    if (activeChar === 'yatta') {
        ctx.fillStyle = '#ffb74d'; ctx.fillRect(player.x, player.y, 24, 50);
    } else if (activeChar === 'looey') {
        ctx.fillStyle = '#fff176'; ctx.fillRect(player.x, player.y, 26, 52);
    } else if (activeChar === 'blot') {
        ctx.fillStyle = '#78909c'; ctx.fillRect(player.x, player.y, 24, 48);
    } else {
        ctx.fillStyle = '#ffb74d'; ctx.fillRect(player.x - 30, player.y, 20, 50);
        ctx.fillStyle = '#fff176'; ctx.fillRect(player.x, player.y - 2, 22, 52);
        ctx.fillStyle = '#78909c'; ctx.fillRect(player.x + 30, player.y + 2, 20, 48);
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
