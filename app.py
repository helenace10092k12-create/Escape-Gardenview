import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Escape Gardenview - Looey Pixel Art",
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
    <title>Looey Pixelated Dialogue Box</title>
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
        }
        #game-box {
            position: relative;
            width: 800px;
            height: 520px;
            background: #0b0514;
            border: 4px solid #512da8;
            box-shadow: 0 0 35px rgba(81, 45, 168, 0.6);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        canvas {
            display: block;
            image-rendering: pixelated; /* Đảm bảo hình chuẩn nét Pixel Art */
            background: #080312;
            border-radius: 8px;
        }
    </style>
</head>
<body>

<div id="game-box">
    <canvas id="looeyCanvas" width="760" height="480"></canvas>
</div>

<script>
const canvas = document.getElementById('looeyCanvas');
const ctx = canvas.getContext('2d');

function drawLooeyDialogue() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // --- 1. TÔ MÀU VÀ VẼ LOOEY PIXELATED THEO TRANH PHÁC THẢO ---
    ctx.save();
    ctx.translate(380, 210); // Đặt tâm ở giữa phía trên khung chat

    // A. 2 TAI BÓNG BAY UỐN CONG (Hình dáng cong theo nét vẽ tay)
    // Tai trái (Màu xanh lá - Green Balloon)
    ctx.fillStyle = '#66bb6a';
    ctx.beginPath();
    ctx.ellipse(-65, -125, 26, 45, -Math.PI / 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#1a0b2e'; ctx.lineWidth = 4; ctx.stroke();
    // Đầu thắt bóng bay
    ctx.fillRect(-85, -165, 10, 8);

    // Tai phải (Màu tím - Purple Balloon)
    ctx.fillStyle = '#ab47bc';
    ctx.beginPath();
    ctx.ellipse(65, -125, 26, 45, Math.PI / 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#1a0b2e'; ctx.lineWidth = 4; ctx.stroke();
    // Đầu thắt bóng bay
    ctx.fillRect(75, -165, 10, 8);

    // B. ĐẦU & KHUÔN MẶT LOOEY (Màu vàng nhạt)
    ctx.fillStyle = '#ffee58';
    ctx.beginPath();
    ctx.arc(0, -35, 65, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#1a0b2e'; ctx.lineWidth = 5; ctx.stroke();

    // C. MẮT LỚN BÓNG LONGLANH CÓ VỆT SỌC (Theo bức vẽ phác)
    ctx.fillStyle = '#111111';
    ctx.beginPath(); ctx.ellipse(-28, -40, 14, 26, 0, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(28, -40, 14, 26, 0, 0, Math.PI * 2); ctx.fill();
    // Vệt sáng dọc mắt
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-32, -55, 4, 25);
    ctx.fillRect(24, -55, 4, 25);

    // D. MÁ HỀ (Trái tím, Phải xanh lá)
    ctx.fillStyle = '#ab47bc';
    ctx.beginPath(); ctx.arc(-42, -15, 10, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#66bb6a';
    ctx.beginPath(); ctx.arc(42, -15, 10, 0, Math.PI * 2); ctx.fill();

    // E. MŨI HỀ ĐỎ TRÒN & MIỆNG CƯỜI HẺM HẲN
    ctx.fillStyle = '#ff1744';
    ctx.beginPath(); ctx.arc(0, -18, 12, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#111'; ctx.lineWidth = 3; ctx.stroke();

    // Miệng cười
    ctx.fillStyle = '#ffffff';
    ctx.beginPath(); ctx.arc(0, 5, 18, 0, Math.PI); ctx.fill();
    ctx.strokeStyle = '#111'; ctx.lineWidth = 3; ctx.stroke();

    // F. KHĂN QUÀNG CỔ / YẾM POLKA DOTS (Trắng chấm bi Tím & Xanh)
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(-60, 80); ctx.lineTo(-30, 25); ctx.lineTo(0, 32);
    ctx.lineTo(30, 25); ctx.lineTo(60, 80); ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#1a0b2e'; ctx.lineWidth = 4; ctx.stroke();

    // Chấm bi trên khăn quàng
    ctx.fillStyle = '#ab47bc'; // Chấm tím
    ctx.beginPath(); ctx.arc(-25, 50, 7, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(20, 65, 8, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#66bb6a'; // Chấm xanh
    ctx.beginPath(); ctx.arc(15, 42, 6, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(-10, 68, 7, 0, Math.PI * 2); ctx.fill();

    ctx.restore();

    // --- 2. KHUNG HỘI THOẠI (DIALOGUE BOX) CHUẨN TRANH BỒ VẼ ---
    // Khung viền ngoài
    ctx.fillStyle = 'rgba(15, 5, 30, 0.92)';
    ctx.fillRect(40, 220, 680, 220);
    ctx.strokeStyle = '#7c4dff';
    ctx.lineWidth = 4;
    ctx.strokeRect(40, 220, 680, 220);

    // Tag Tên Nhân Vật "Looey" ở góc trên bên phải khung
    ctx.fillStyle = '#311b92';
    ctx.fillRect(580, 195, 120, 30);
    ctx.strokeStyle = '#7c4dff';
    ctx.lineWidth = 2;
    ctx.strokeRect(580, 195, 120, 30);
    ctx.fillStyle = '#ffb74d';
    ctx.font = 'bold 16px Courier New';
    ctx.textAlign = 'center';
    ctx.fillText("Looey", 640, 216);

    // Nội dung đoạn chat
    ctx.fillStyle = '#00e676';
    ctx.font = '16px Courier New';
    ctx.textAlign = 'left';
    ctx.fillText("* Chat is in here *", 70, 260);
    ctx.fillStyle = '#e0f2f1';
    ctx.fillText("My balloons almost popped right at the finale! Haha!", 70, 300);

    // Nút Next
    ctx.fillStyle = '#311b92';
    ctx.fillRect(560, 380, 130, 34);
    ctx.strokeStyle = '#ab47bc';
    ctx.lineWidth = 2;
    ctx.strokeRect(560, 380, 130, 34);
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 13px Courier New';
    ctx.fillText("Next [Space] >", 572, 402);
}

drawLooeyDialogue();
</script>
</body>
</html>
"""

components.html(game_code, height=560)
