# app.py
import streamlit as st
import ui

st.set_page_config(page_title="SNSソーシャルリスニング", layout="wide")

page_options = {
    "ダッシュボード": "dashboard",
    "新規リスニングジョブ作成": "create_job",
}

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

current_index = list(page_options.values()).index(st.session_state["page"])
selected = st.sidebar.radio(
    "画面を選択してください",
    list(page_options.keys()),
    index=current_index
)

if page_options[selected] != st.session_state["page"]:
    st.session_state["page"] = page_options[selected]
    st.rerun()

if st.session_state["page"] == "dashboard":
    ui.dashboard()
elif st.session_state["page"] == "create_job":
    ui.create_job()
