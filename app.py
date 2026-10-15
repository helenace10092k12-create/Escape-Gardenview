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
                <div id="
