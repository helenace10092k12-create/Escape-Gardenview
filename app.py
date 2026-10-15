import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird Test", page_icon="🐦", layout="centered")

st.title("🐦 Flappy Bird - Streamlit Test")
st.write("Bấm **[SPACE]** (Phím khoảng trắng) hoặc **Click chuột** vào khung game để nhảy!")

# Mã HTML/JavaScript dựng game Flappy Bird mượt mà trên Canvas
flappy_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background-color: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', Courier, monospace;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #70c5ce;
            image-rendering: pixelated;
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="320" height="480"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Biến trạng thái
let birdY = 200;
let velocity = 0;
let gravity = 0.25;
let jump = -4.5;
let score = 0;
let gameOver = false;

// Ống nước
let pipes = [];
let pipeWidth = 50;
let pipeGap = 120;
let frameCount = 0;

function resetGame() {
    birdY = 200;
    velocity = 0;
    score = 0;
    pipes = [];
    gameOver = false;
}

// Xử lý sự kiện bấm phím / click
window.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        if (gameOver) {
            resetGame();
        } else {
            velocity = jump;
        }
    }
});

canvas.addEventListener("click", function() {
    if (gameOver) {
        resetGame();
    } else {
        velocity = jump;
    }
});

function drawBird() {
    // Vẽ chim dạng Pixel Art vàng
    ctx.fillStyle = "#ffeb3b";
    ctx.fillRect(80, birdY, 20, 20);
    ctx.fillStyle = "#ff9800";
    ctx.fillRect(95, birdY + 8, 8, 6); // Mỏ
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(90, birdY + 2, 6, 6); // Mắt
    ctx.fillStyle = "#000000";
    ctx.fillRect(93, birdY + 4, 2, 2);
}

function updatePipes() {
    if (frameCount % 90 === 0) {
        let topHeight = Math.floor(Math.random() * (canvas.height - pipeGap - 100)) + 30;
        pipes.push({
            x: canvas.width,
            top: topHeight,
            bottom: canvas.height - topHeight - pipeGap,
            passed: false
        });
    }

    for (let i = 0; i < pipes.length; i++) {
        let p = pipes[i];
        p.x -= 2;

        // Vẽ ống trên
        ctx.fillStyle = "#75c043";
        ctx.fillRect(p.x, 0, pipeWidth, p.top);
        ctx.strokeStyle = "#000";
        ctx.strokeRect(p.x, 0, pipeWidth, p.top);

        // Vẽ ống dưới
        ctx.fillRect(p.x, canvas.height - p.bottom, pipeWidth, p.bottom);
        ctx.strokeRect(p.x, canvas.height - p.bottom, pipeWidth, p.bottom);

        // Va chạm
        if (
            80 + 20 > p.x && 80 < p.x + pipeWidth &&
            (birdY < p.top || birdY + 20 > canvas.height - p.bottom)
        ) {
            gameOver = true;
        }

        // Tính điểm
        if (p.x + pipeWidth < 80 && !p.passed) {
            score++;
            p.passed = true;
        }
    }

    // Xóa ống cũ
    if (pipes.length > 0 && pipes[0].x < -pipeWidth) {
        pipes.shift();
    }
}

function drawScore() {
    ctx.fillStyle = "#ffffff";
    ctx.font = "20px 'Courier New'";
    ctx.fillText("Score: " + score, 10, 30);
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Nền cỏ phía dưới
    ctx.fillStyle = "#ded895";
    ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

    if (!gameOver) {
        velocity += gravity;
        birdY += velocity;

        if (birdY + 20 >= canvas.height - 20 || birdY <= 0) {
            gameOver = true;
        }

        updatePipes();
        drawBird();
        drawScore();
        frameCount++;
    } else {
        ctx.fillStyle = "#ffffff";
        ctx.font = "24px 'Courier New'";
        ctx.fillText("GAME OVER", 90, 200);
        ctx.font = "14px 'Courier New'";
        ctx.fillText("Click / Space to Restart", 60, 240);
        ctx.fillText("Final Score: " + score, 85, 270);
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>

</body>
</html>
"""

# Hiển thị game trong Streamlit
components.html(flappy_code, height=520)
