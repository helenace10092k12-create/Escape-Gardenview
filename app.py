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

# --------------------------------------------------------------------------
# BỒ ĐỔI LINK NÀY THÀNH LINK RAW ẢNH LOOEY TRÊN GITHUB CỦA BỒ NHA:
# Ví dụ: https://raw.githubusercontent.com/<user>/<repo>/main/1000009227.png
# --------------------------------------------------------------------------
LOOEY_IMAGE_URL = "https://raw.githubusercontent.com/username/repository/main/1000009227.png"

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Escape Gardenview</title>
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

        /* OVERLAY NỔI NGUYÊN BỨC ẢNH PIXEL CỦA LOOEY */
        #looey-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 800px;
            height: 320px;
            z-index: 50;
            display: none;
            pointer-events: none;
        }

        #looey-img {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: bottom;
            image-rendering: pixelated;
        }

        #looey-text-area {
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
        }

        #looey-text-content {
            color: #231205;
            font-weight: bold;
            font-size: 13px;
            line-height: 1.35;
        }

        .dialogue-btns { display: flex; justify-content: flex-end; }
        .action-btn {
            background: #311b92; color: #ffeb3b; border: 2px solid #ab47bc;
            padding: 3px 10px; font-size: 10px; cursor: pointer; border-radius: 4px; font-weight: bold;
        }
        .action-btn:hover { background: #512da8; color: #fff; }

        /* KHUNG CHAT THƯỜNG DÀNH CHO DẪN CHUYỆN */
        #normal-chat-box {
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
        }
        #normal-speaker { color: #ffb74d; font-weight: bold; font-size: 11px; margin-bottom: 2px; }
        #normal-text { color: #00e676; font-size: 11px; line-height: 1.3; }
    </style>
</head>
<body>

<div id="game-box">
    <div id="top-ui">
        <div class="title" id="game-title">GARDENVIEW: HALLOWEEN ESCAPE</div>
        <div class="ui-right-group">
            <div class="hud-buttons">
                <button class="toon-btn" id="btn-yatta" onclick="switch
