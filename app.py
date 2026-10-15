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
        .title { color: #ff7043; font-weight: bold; font-size: 13px; letter-spacing: 1px; }
        .hud-buttons {
            display: flex;
            gap: 5px;
        }
        .toon-btn {
            background: #1a0b2e; color: #d1c4e9; border: 1px solid #7c4dff;
            padding: 3px 8px; font-size: 10px; cursor: pointer; border-radius: 3px;
        }
        .toon-btn.active { background: #651fff; color: #fff; border-weight: bold; }
        
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

        /* Character Info Pop-up (Hiển thị 10 giây khi đổi nhân vật) */
        #info-popup {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 5, 30, 0.92);
            border: 2px solid #00e676;
            padding: 10px 20px;
            border-radius: 6px;
            text-align: center;
            z-index: 30;
            display: none;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.5);
        }
        #info-title { color: #00e676; font-size: 13px; font-weight: bold; margin-bottom: 3px; }
        #info-desc { color: #e0f2f1; font-size: 11px; }

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
        #speaker { color: #ffb74d; font-weight: bold; font-size: 14px; margin-bottom: 4px; }
        #dialogue-text { color: #00e676; font-size: 13px; line-height: 1.4; height: 60px; }
        
        .dialogue-btns {
            display: flex;
            gap: 10px;
        }
        .action-btn {
            background: #311b92; color: #ede7f6; border: 1px solid #7c4dff;
            padding: 5px 12px; font-size: 11px; cursor: pointer; border-radius: 4px;
        }
        .action-btn:hover { background: #512da8; }
    </style>
</head>
<body>

<div id="game-box">
    <div id="top-ui">
        <div class="title">GARDENVIEW: HALLOWEEN ESCAPE (LOCKED AWAY)</div>
        <div class="hud-buttons">
            <button class="toon-btn active" id="btn-yatta" onclick="switchCharacter('yatta')">Yatta</button>
            <button class="toon-btn" id="btn-looey" onclick="switchCharacter('looey')">Looey</button>
            <button class="toon-btn" id="btn-blot" onclick="switchCharacter('blot')">Blot</button>
            <button class="toon-btn" id="btn-trio" onclick="switchCharacter('trio')">Circus Trio</button>
        </div>
    </div>

    <div id="canvas-holder">
        <canvas id="gameCanvas" width="800" height="380"></canvas>
        <div id="crt-overlay"></div>
        
        <!-- Bảng thông tin nhân vật xuất hiện 10 giây -->
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

let currentStep = 0;
let activeChar = 'yatta';
let popupTimer = null;

// Thông tin chi tiết nhân vật khi chọn
const charInfoData = {
    yatta: { name: "YATTA (Acrobatic)", desc: "Dẻo dai, linh hoạt, chuyên leo trèo các khu vực cao." },
    looey: { name: "LOOEY (Fast Runner)", desc: "Chạy cực nhanh, né tránh các Twisted bám đuổi sát nút." },
    blot: { name: "BLOT (Mime & Clone)", desc: "Im lặng tuyệt đối, có khả năng tạo phân thân (clone) đánh lừa quái." },
    trio: { name: "CIRCUS TRIO", desc: "Sức mạnh đoàn kết cả ba thành viên để sinh tồn trong Gardenview!" }
};

// Cốt truyện mở đầu
const introScript = [
    { speaker: "NARRATOR", text: "Buổi biểu diễn trước các Toon vừa kết thúc tốt đẹp. Circus Trio bước về phòng thay đồ để nghỉ ngơi sau tiếng vỗ tay vang dội." },
    { speaker: "YATTA", text: "Phù... hôm nay quẩy sung thật đấy! Mấy bạn Toon cổ vũ nhiệt tình ghê luôn." },
    { speaker: "LOOEY", text: "Bóng bay của tui suýt nổ tung lúc cuối màn diễn! Haha!" },
    { speaker: "BLOT", text: "(Gật đầu im lặng, mỉm cười nhẹ nhàng trong góc phòng)." },
    { speaker: "NARRATOR", text: "*RẦM!* Đột nhiên, cánh cửa sắt phòng thay đồ tự động sập đóng lại chặt cứng!" },
    { speaker: "BLOT", text: "Khoan đã... Đèn tắt hết rồi! Blackout toàn tập?!" },
    { speaker: "Yatta", text: "Ơ kìa... cái gì đang phát sáng ở giữa sàn nhà thế kia? Một cái nút màu đỏ kỳ lạ..." },
    { speaker: "NARRATOR", text: "Vì tò mò, Yatta bước đến và vô tình chạm vào nút bấm..." },
    { speaker: "NARRATOR", text: "*VÉO VÉO!* Một cánh cổng ảo xoáy sâu mở ra! Cả ba hốt hoảng bám chặt vào đồ đạc nhưng lực hút quá mạnh..." },
    { speaker: "NARRATOR", text: "...Và rồi, cả nhóm bị 'nhả' phăng xuống một nơi lạnh lẽo. Gardenview đây sao? Không... nó tồi tàn và âm u đến rợn ngáy!" },
    { speaker: "SYSTEM", text: "WELCOME TO GARDENVIEW ESCAPE GAME. COLLECT 8 GOLDEN KEYS TO FORM THE PUMPKIN KEY AND ESCAPE!" },
    { speaker: "SYSTEM", text: "Nhiệm vụ của bạn: Khám phá các căn phòng, mở rương, né tránh các Twisted nguy hiểm và tìm kiếm trợ giúp từ các Toon còn sống sót!" }
];

function switchCharacter(char) {
    activeChar = char;
    document.querySelectorAll('.toon-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('btn-' + char).classList.add('active');
    
    showCharPopup(char);
}

function showCharPopup(char) {
    const info = charInfoData[char];
    const popup = document.getElementById('info-popup');
    document.getElementById('info-title').innerText = info.name;
    document.getElementById('info-desc').innerText = info.desc;
    
    popup.style.display = 'block';
    
    if (popupTimer) clearTimeout(popupTimer);
    popupTimer = setTimeout(() => {
        popup.style.display = 'none';
    }, 10000); // Ẩn sau 10 giây đúng yêu cầu
}

function nextLine() {
    currentStep++;
    if (currentStep >= introScript.length) {
        currentStep = introScript.length - 1;
        document.getElementById('dialogue-text.innerText') = "Đã vào sảnh chính Gardenview bỏ hoang! Hãy sẵn sàng khám phá màn chơi tiếp theo...";
    }
    updateDialogue();
}

function updateDialogue() {
    const data = introScript[currentStep];
    document.getElementById('speaker').innerText = data.speaker;
    document.getElementById('dialogue-text').innerText = data.text;
}

// Render Side-view nền tảng phòng thay đồ / Gardenview
function gameLoop() {
    ctx.fillStyle = '#06030c';
    ctx.fillRect(0, 0, 800, 380);

    // Vẽ nền ô vuông retro FNAF
    ctx.fillStyle = '#0f071a';
    for(let x = 0; x < 800; x += 40) {
        for(let y = 0; y < 380; y += 40) {
            if ((x/40 + y/40) % 2 === 0) ctx.fillRect(x, y, 40, 40);
        }
    }

    // Vẽ sàn nhà
    ctx.fillStyle = '#281145';
    ctx.fillRect(0, 320, 800, 60);
    ctx.fillStyle = '#7c4dff';
    ctx.fillRect(0, 320, 800, 4);

    // Vẽ nhóm Circus Trio đứng tương ứng nhân vật active
    let drawX = 350;
    if (activeChar === 'yatta') {
        ctx.fillStyle = '#ffb74d'; ctx.fillRect(drawX, 260, 24, 60); // Yatta
    } else if (activeChar === 'looey') {
        ctx.fillStyle = '#fff176'; ctx.fillRect(drawX, 255, 26, 65); // Looey
    } else if (activeChar === 'blot') {
        ctx.fillStyle = '#78909c'; ctx.fillRect(drawX, 262, 24, 58); // Blot
    } else {
        // Circus Trio (cả 3 đứng chung)
        ctx.fillStyle = '#ffb74d'; ctx.fillRect(drawX - 40, 260, 22, 60);
        ctx.fillStyle = '#fff176'; ctx.fillRect(drawX, 255, 24, 65);
        ctx.fillStyle = '#78909c'; ctx.fillRect(drawX + 40, 262, 22, 58);
    }

    requestAnimationFrame(gameLoop);
}

// Khởi tạo
updateDialogue();
showCharPopup('yatta'); // Hiện bảng Yatta lúc đầu 10s
gameLoop();
</script>
</body>
</html>
"""

components.html(game_code, height=620)
