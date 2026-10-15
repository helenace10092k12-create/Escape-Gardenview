import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Dandy's World: Circus Mystery", page_icon="🎪", layout="centered")

# --- KHỞI TẠO TÌNH TRẠNG GAME ---
if "lang" not in st.session_state:
    st.session_state.lang = "VIE"
if "scene" not in st.session_state:
    st.session_state.scene = "dressing_room"

# --- TỪ ĐỂN SONG NGỮ ---
TEXT = {
    "VIE": {
        "title": "🎪 DANDY'S WORLD: BÍ ẨN PHÒNG THAY ĐỒ",
        "dressing_room": "Buổi biểu diễn vừa kết thúc thành công! Yatta, Looey và Blot cùng quay trở lại phòng thay đồ. Nhưng ngay khi Blot vừa bước qua cánh cửa...",
        "event_blackout": "💥 RẮC! Cánh cửa sắt tự động sập xuống và khóa chặt! Đèn vụt tắt hoàn toàn... Một màn hình hệ thống màu đỏ lóe lên trong bóng tối!",
        "btn_next": "Khám phá màn hình Hệ Thống",
        "system_msg": "🤖 [HỆ THỐNG]: Chào mừng Circus Trio. Các bạn đã bị chuyển đến Gardenview bỏ hoang. Hãy sống sót!",
        "btn_restart": "Chơi lại từ đầu",
    },
    "ENG": {
        "title": "🎪 DANDY'S WORLD: DRESSING ROOM MYSTERY",
        "dressing_room": "The show was a huge success! Yatta, Looey, and Blot return to the dressing room. But as soon as Blot steps inside...",
        "event_blackout": "💥 BANG! The iron door slams shut and locks! All lights go out... A glowing red system screen appears in the dark!",
        "btn_next": "Inspect the System Screen",
        "system_msg": "🤖 [SYSTEM]: Welcome Circus Trio. You have been transported to abandoned Gardenview. Survive!",
        "btn_restart": "Restart Game",
    }
}

# --- NÚT ĐỔI NGÔN NGỮ ---
col_title, col_lang = st.columns([4, 1])
with col_lang:
    if st.button("🌐 " + ("English" if st.session_state.lang == "VIE" else "Tiếng Việt")):
        st.session_state.lang = "ENG" if st.session_state.lang == "VIE" else "VIE"
        st.rerun()

L = TEXT[st.session_state.lang]

# --- GIAO DIỆN CHÍNH ---
st.title(L["title"])

# --- LOGIC CHUYỂN CẢNH ---
if st.session_state.scene == "dressing_room":
    st.write(L["dressing_room"])
    st.error(L["event_blackout"])
    if st.button(L["btn_next"]):
        st.session_state.scene = "system_world"
        st.rerun()

elif st.session_state.scene == "system_world":
    st.info(L["system_msg"])
    if st.button(L["btn_restart"]):
        st.session_state.scene = "dressing_room"
        st.rerun()
