import streamlit as st
from datetime import datetime
import html
import uuid

st.set_page_config(
    page_title="信頼度スコアSNS",
    page_icon="🛡️",
    layout="wide",
)

# =========================
# 白基調・信頼度スコアSNS
# =========================
st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
        color: #172033;
    }
    [data-testid="stHeader"] {
        background: rgba(245,247,251,.92);
    }
    .block-container {
        max-width: 1120px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, p, label {
        color: #172033;
    }
    .hero {
        background: linear-gradient(115deg, #ffffff 0%, #edf4ff 100%);
        border: 1px solid #dce6f5;
        border-radius: 22px;
        padding: 1.5rem 1.7rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 8px 28px rgba(34, 67, 120, .06);
    }
    .hero-kicker {
        color: #4776c5;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .15em;
    }
    .hero-title {
        color: #14213d;
        font-size: 2.15rem;
        font-weight: 800;
        margin: .35rem 0 .35rem 0;
    }
    .hero-sub {
        color: #586782;
        font-size: 1rem;
    }
    .post-card {
        background: #ffffff;
        border: 1px solid #e1e7f0;
        border-radius: 17px;
        padding: 1rem 1.15rem;
        margin: .55rem 0 .75rem 0;
        box-shadow: 0 4px 16px rgba(24, 44, 80, .045);
    }
    .post-author {
        color: #315fa8;
        font-weight: 750;
    }
    .post-time {
        color: #7a879b;
        font-size: .8rem;
    }
    .post-text {
        color: #202b3e;
        font-size: 1.02rem;
        line-height: 1.7;
        margin: .7rem 0;
        overflow-wrap: anywhere;
    }
    .score-pill {
        display: inline-block;
        padding: .28rem .65rem;
        border-radius: 999px;
        font-size: .84rem;
        font-weight: 750;
        margin-top: .25rem;
    }
    .score-high {
        background: #e8f8ef;
        color: #167346;
        border: 1px solid #c4ecd4;
    }
    .score-mid {
        background: #fff5dc;
        color: #8a5a00;
        border: 1px solid #f2dfab;
    }
