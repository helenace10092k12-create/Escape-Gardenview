import streamlit as st
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Escape Gardenview",
    page_icon="🎪",
    layout="centered"
)

# --- CSS GIẢ LẬP GIAO DIỆN PIXEL / RETRO HORROR ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Press Start 2P', monospace;
        background-color: #0e0e12;
        color: #e0e0e0;
    }
    
    .stButton>button {
        background-color: #2b1020;
        color: #ff4b4b;
        border: 2px solid #ff4b4b;
        font-family: 'Press Start 2P', monospace;
        padding: 10px;
        border-radius: 0px;
        box-shadow: 3px 3px 0px #800000;
    }
    
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: #000000;
    }

    .comic-frame {
        border: 4px solid #444;
        background-color: #1a1a24;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO SESSION STATE ---
if "lang" not in st.session_state:
    st.session_state.lang = "ENG"  # Mặc định Tiếng Anh

if "frame" not in st.session_state:
    st.session_state.frame = 1  # Tiến trình khung truyện comic mở đầu

# --- TỪ ĐỂN SONG NGỮ (ENG MẶC ĐỊNH) ---
TEXT = {
    "ENG": {
        "title": "🎪 ESCAPE GARDENVIEW",
        "btn_lang": "🌐 Tiếng Việt",
        "frame_1": "The show at Gardenview has just ended! Yatta, Looey, and Blot walk back towards the dressing room, chatting happily after a great performance.",
        "frame_2": "SUDDENLY! The heavy iron door SLAMS SHUT on its own—without any draft! 💥\nThen... TOTAL BLACKOUT.",
        "frame_3": "In the pitch-black darkness, a mysterious glowing virtual button appears out of nowhere in front of them.",
        "frame_4": "Yatta curiously presses the button... Instantly, a swirling dimensional portal tears open! A powerful force pulls all three of them in!",
        "frame_5": "They frantically grab onto doors and pipes trying to hold on, but the force is too strong... *SWOOSH!*",
        "frame_6": "*OOF!* 💥 The trio tumbles out of the rift and lands flat on their butts in a dark, rotting, and completely abandoned Gardenview...",
        "btn_next": "Next Panel ➔",
        "btn_start_game": "🎮 Start Exploration",
        "yatta_talk": "Yatta: 'Ouch... my tail... Is everyone alright?'",
        "looey_talk": "Looey: 'Where... where are we? This doesn't look like our dressing room at all!'",
        "blot_talk": "Blot: '...The ink in the air feels cold and twisted. Stay on guard.'",
    },
    "VIE": {
        "title": "🎪 ESCAPE GARDENVIEW",
        "btn_lang": "🌐 English",
        "frame_1": "Buổi biểu diễn tại Gardenview vừa kết thúc! Nhóm Yatta, Looey và Blot cùng nhau vui vẻ rảo bước quay về phòng thay đồ.",
        "frame_2": "ĐỘT NHIÊN! Cánh cửa sắt nặng nề tự động SẬP LẠI dù không hề có một luồng gió nào! 💥\nNgay sau đó... Màn đêm bao trùm (Blackout hoàn toàn).",
        "frame_3": "Trong bóng tối mịt mùng, một nút bấm ảo phát sáng bí ẩn tự nhiên hiện lên ngay trước mặt cả nhóm.",
        "frame_4": "Yatta tò mò nhấn vào nút... Ngay lập tức, một cánh cổng dịch chuyển xoáy sâu mở ra! Luồng sức mạnh khủng khiếp hút cả ba vào trong!",
        "frame_5": "Cả nhóm cuống quýt bám chặt vào khung cửa và ống nước để níu lại, nhưng sức hút quá mạnh... *XOÁY!*",
        "frame_6": "*ÁI DA!* 💥 Cả ba té dập đít từ cánh cổng xuống một hành lang Gardenview tối tăm, mục nát và hoàn toàn bị bỏ hoang...",
        "btn_next": "Khung tiếp theo ➔",
        "btn_start_game": "🎮 Bắt đầu khám phá",
        "yatta_talk": "Yatta: 'Ái da... cái đuôi của tui... Mọi người có sao không?'",
        "looey_talk": "Looey: 'Đâu... đây là đâu vậy? Chỗ này đâu phải phòng thay đồ của mình!'",
        "blot_talk": "Blot: '...Dòng mực trong không khí cảm giác rất lạnh và biến dạng. Cẩn thận đấy.'",
    }
}

# --- NÚT ĐỔI NGÔN NGỮ ---
col_head, col_btn = st.columns([3, 1])
with col_head:
    st.title(TEXT[st.session_state.lang]["title"])
with col_btn:
    if st.button(TEXT[st.session_state.lang]["btn_lang"]):
        st.session_state.lang = "VIE" if st.session_state.lang == "ENG" else "ENG"
        st.rerun()

L = TEXT[st.session_state.lang]

# --- HIỂN THỊ CÁC NHÂN VẬT ---
st.write("### 🎪 Circus Trio")
col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists("yatta.png"):
        st.image("yatta.png", caption="Yatta", width=120)
    else:
        st.info("Yatta")

with col2:
    if os.path.exists("looey.png"):
        st.image("looey.png", caption="Looey", width=120)
    else:
        st.info("Looey")

with col3:
    if os.path.exists("blot.png"):
        st.image("blot.png", caption="Blot", width=120)
    else:
        st.info("Blot")

st.divider()

# --- MỞ ĐẦU DẠNG COMIC FRAME ---
st.subheader("📖 Story Intro")

# Khung truyện dạng Comic Panel
current_frame = st.session_state.frame

if current_frame >= 1:
    st.info(f"**Panel 1:** {L['frame_1']}")
if current_frame >= 2:
    st.warning(f"**Panel 2:** {L['frame_2']}")
if current_frame >= 3:
    st.error(f"**Panel 3:** {L['frame_3']}")
if current_frame >= 4:
    st.error(f"**Panel 4:** {L['frame_4']}")
if current_frame >= 5:
    st.error(f"**Panel 5:** {L['frame_5']}")
if current_frame >= 6:
    st.success(f"**Panel 6:** {L['frame_6']}")
    if os.path.exists("gardenview.png"):
        st.image("gardenview.png", caption="Abandoned Gardenview Corridor", use_column_width=True)
    
    st.write("---")
    st.write(L["yatta_talk"])
    st.write(L["looey_talk"])
    st.write(L["blot_talk"])

# Nút bấm chuyển khung truyện
if current_frame < 6:
    if st.button(L["btn_next"]):
        st.session_state.frame += 1
        st.rerun()
else:
    if st.button(L["btn_start_game"]):
        st.success("Bắt đầu vào Gameplay di chuyển & sinh tồn!")
    
