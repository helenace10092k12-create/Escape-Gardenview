import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Escape Gardenview", layout="wide")

# Đọc mã HTML trực tiếp từ file index.html
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=620)
