import streamlit as st
import streamlit.components.v1 as components
import base64

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

# TOÀN BỘ MÃ NGUỒN GAME ĐÃ ĐƯỢC MÃ HÓA BASE64 CHUẨN SẠCH 100% KHÔNG BAO GIỜ BỊ LỖI CÚ PHÁP
encoded_game = """
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0
PSJVVEYtOCI+CiAgICA8dGl0bGU+RXNjYXBlIEdhcmRlbnZpZXc8L3RpdGxlPgogICAgPHN0eWxl
PgogICAgICAgICogeyBib3gtc2l6aW5nOiBib3JkZXItYm94OyBtYXJnaW46IDA7IHBhZGRpbmc6
IDA7IHVzZXItc2VsZWN0OiBub25lOyB9CiAgICAgICAgYm9keSB7CiAgICAgICAgICAgIGJhY2tn
cm91bmQtY29sb3I6ICMwMzAxMDU7CiAgICAgICAgICAgIGNvbG9yOiAjZmZmOwogICAgICAgICAg
ICBmb250LWZhbWlseTogJ0NvdXJpZXIgTmV3JywgQ291cmllciwgbW9ub3NwYWNlOwogICAgICAg
ICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjsK
ICAgICAgICAgICAgYWxpZ
