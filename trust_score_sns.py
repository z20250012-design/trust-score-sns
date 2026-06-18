```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

st.set_page_config(
    page_title="信頼度スコアSNS Ver.5",
    page_icon="🛡️",
    layout="wide"
)

DATA_FILE = "posts.json"

# ----------------------
# データ保存
# ----------------------

def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

# ----------------------
# 信頼度計算
# ----------------------

def calculate_trust(text):

    score = 50

    positive_words = [
        "出典",
        "証拠",
        "研究",
        "論文",
        "統計",
        "データ"
    ]

    negative_words = [
        "絶対",
        "100%",
        "必ず",
        "確実",
        "噂"
    ]

    for word in positive_words:
        if word in text:
            score += 8

    for word in negative_words:
        if word in text:
            score -= 8

    return max(0, min(score, 100))

# ----------------------
# 初期化
# ----------------------

if "posts" not in st.session_state:
    st.session_state.posts = load_posts()

# ----------------------
# タイトル
# ----------------------

st.title("🛡️ 信頼度スコアSNS Ver.5")
st.caption("誤情報対策を目的とした探究用SNS")

# ----------------------
# サイドバー
# ----------------------

with st.sidebar:

    st.header("👤 ユーザー")

    username = st.text_input(
        "ユーザー名",
        value="匿名ユーザー"
    )

    st.markdown("---")

    st.subheader("📊 統計")

    st.write(f"投稿数: {len(st.session_state.posts)}")

# ----------------------
# 投稿
# ----------------------

st.subheader("✏️ 投稿")

post_text = st.text_area(
    "内容を書いてください"
)

if st.button("投稿する"):

    if post_text.strip():

        trust = calculate_trust(post_text)

        post = {
            "user": username,
            "text": post_text,
            "trust": trust,
            "likes": 0,
            "reports": 0,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        st.session_state.posts.append(post)

        save_posts(st.session_state.posts)

        st.success("投稿しました")

# ----------------------
# グラフ
# ----------------------

st.subheader("📈 信頼度分析")

if len(st.session_state.posts) > 0:

    df = pd.DataFrame(st.session_state.posts)

    fig = px.histogram(
        df,
        x="trust",
        nbins=10,
        title="信頼度スコア分布"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# タイムライン
# ----------------------

st.subheader("📱 タイムライン")

sorted_posts = sorted(
    st.session_state.posts,
    key=lambda x: x.get("trust", 0),
    reverse=True
)

for i, post in enumerate(sorted_posts):

    trust = post.get("trust", 0)

    with st.container():

        st.markdown(f"### 👤 {post['user']}")
        st.caption(post["time"])

        st.write(post["text"])

        st.progress(trust)

        if trust >= 80:
            st.success(f"🟢 信頼度 {trust}")
        elif trust >= 60:
            st.info(f"🟡 信頼度 {trust}")
        else:
            st.error(f"🔴 注意: 信頼度 {trust}")

        if trust < 60:
            st.warning("⚠ 注意ラベル: 未確認情報の可能性があります")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(
                f"👍 {post['likes']}",
                key=f"like{i}"
            ):
                post["likes"] += 1
                save_posts(st.session_state.posts)
                st.rerun()

        with col2:
            if st.button(
                f"🚨 通報 {post['reports']}",
                key=f"report{i}"
            ):
                post["reports"] += 1
                save_posts(st.session_state.posts)
                st.rerun()

        with col3:
            st.write(f"🏆順位 #{i+1}")

        st.divider()
```
