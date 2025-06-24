# frontend/app.py
import streamlit as st
from run_java import run_pattern_search

st.set_page_config(page_title="🔍 Pattern Search Engine", layout="centered")

st.markdown("<h1 style='text-align: center;'>🔍 MiniFinder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Search patterns using <b>Naive</b>, <b>KMP</b>, or <b>Boyer-Moore</b> algorithms</p>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([1, 1])
with col1:
    algorithm = st.selectbox("🧠 Choose Algorithm", ["Naive", "KMP", "Boyer-Moore"])
with col2:
    pattern = st.text_input("🔎 Enter Pattern to Search")

text = st.text_area("📝 Enter Paragraph/Text", height=200)

if st.button("🚀 Search"):
    if not text or not pattern:
        st.warning("⚠️ Please enter both text and pattern.")
    else:
        with st.spinner("Running algorithm..."):
            result = run_pattern_search(algorithm.lower(), text.strip(), pattern.strip())

        if "error" in result:
            st.error(f"Java Error: {result['error']}")
        else:
            match_positions = result["positions"]
            match_count = result["matches"]
            time_ms = result["time_ms"]

            if match_count == 0:
                st.info("❌ Pattern not found.")
            else:
                highlighted = ""
                i = 0
                p_len = len(pattern)
                while i < len(text):
                    if i in match_positions:
                        highlighted += f"<mark style='background-color: yellow;'>{text[i:i+p_len]}</mark>"
                        i += p_len
                    else:
                        highlighted += text[i]
                        i += 1

                st.markdown("### ✅ Results")
                st.markdown(f"**🎯 Accuracy:** `100%` (exact match)")
                st.markdown(f"**🔢 Matches Found:** `{match_count}`")
                st.markdown(f"**⏱️ Time Taken:** `{time_ms} ms`")
                st.markdown("**📌 Highlighted Paragraph:**", unsafe_allow_html=True)
                st.markdown(f"<div style='line-height: 1.8;'>{highlighted}</div>", unsafe_allow_html=True)
