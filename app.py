import streamlit as st
import numpy as np
from data import USERS
from engine import get_stylometry, get_fingerprint_similarity, evaluate_anomaly

st.set_page_config(page_title="AuthPrint Engine", layout="wide")
st.title("AuthPrint: Identity Mismatch Engine")
st.markdown("**First Dollar Moderation** | *Checking identity, not just AI patterns.*")

st.sidebar.header("1. Target Profile")
selected_user = st.sidebar.selectbox("Select Baseline", list(USERS.keys()))
history = USERS[selected_user]

st.sidebar.subheader("Established Fingerprint")
for tweet in history:
    st.sidebar.caption(f"- {tweet}")

st.subheader("2. Analyze New Submission")
new_tweet = st.text_area("Paste new bounty submission here:", height=100)

if st.button("Run Identity Check", type="primary"):
    if not new_tweet.strip():
        st.error("Input required.")
    else:
        with st.spinner("Analyzing stylometry and N-Gram footprints..."):
            hist_stats_list = [get_stylometry(t) for t in history]
            avg_hist_stats = {
                "avg_word_len": round(np.mean([s["avg_word_len"] for s in hist_stats_list]), 2),
                "punct_ratio": round(np.mean([s["punct_ratio"] for s in hist_stats_list]), 3),
                "upper_ratio": round(np.mean([s["upper_ratio"] for s in hist_stats_list]), 3)
            }
            new_stats = get_stylometry(new_tweet)
            sim_score = get_fingerprint_similarity(history, new_tweet)
            
            verdict = evaluate_anomaly(avg_hist_stats, new_stats, sim_score)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("N-Gram Match", f"{sim_score} / 1.0")
            col2.metric("Stylometry", "Deviated" if abs(sim_score) < 0.4 else "Stable")
            col3.metric("Anomaly Score", f"{verdict.get('anomaly_score', 0)} / 100")
            
            if verdict.get("flagged"):
                st.error("🚨 FLAG: IDENTITY MISMATCH DETECTED")
            else:
                st.success("✅ PASS: BEHAVIORAL FINGERPRINT MATCHES")
                
            st.info(f"**Diagnostic:** {verdict.get('reasoning', '')}")