import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="信頼度スコアSNS Ver.6",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# デザイン
# -------------------------

st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
    color:white;
}

.post-card{
    background-color:#161B22;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    border:1px solid #30363D;
}

.trust-high{
    color:#00FF88;
    font-weight:bold;
}

.trust-medium{
    color:#FFD700;
    font-weight:bold;
}

.trust-low{
    color:#FF4B4B;
    font-weight:bold;
}

.big-title{
    font-size:40px;
    font-weight:bold;
    color:#4DA6FF;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# 初期化
# -------------------------

if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "user":"運営",
            "text":"ようこそ！信頼度スコアSNSへ",
            "trust":100,
            "likes":0,
            "reports":0,
            "time":datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]

# -------------------------
# 信頼度計算
# -------------------------

def calculate_trust(text):

    score = 50

    positive_words = [
        "出典","証拠","研究",
        "論文","統計","データ"
    ]

    negative_words = [
        "絶対","100%",
        "必ず","確実","噂"
    ]

    reasons = []

    for word in positive_words:
        if word in text:
            score += 8
            reasons.append(f"✅ {word}を含む")

    for word in negative_words:
        if word in text:
            score -= 8
            reasons.append(f"⚠ {word}を含む")

    score = max(0,min(score,100))

    return score,reasons

# -------------------------
# タイトル
# -------------------------

st.markdown(
    '<p class="big-title">🛡️ 信頼度スコアSNS Ver.6</p>',
    unsafe_allow_html=True
)

st.caption("誤情報対策を目的とした探究用SNS")

# -------------------------
# サイドバー
# -------------------------

with st.sidebar:

    st.header("👤 ユーザー")

    username = st.text_input(
        "ユーザー名",
        value="匿名ユーザー"
    )

    st.markdown("---")

    st.subheader("📊 統計")

    st.metric(
        "投稿数",
        len(st.session_state.posts)
    )

# -------------------------
# 投稿
# -------------------------

st.subheader("✏️ 投稿する")

post_text = st.text_area(
    "投稿内容を入力"
)

if st.button("投稿"):

    if post_text.strip():

        trust,reasons = calculate_trust(post_text)

        st.session_state.posts.append({

            "user":username,
            "text":post_text,
            "trust":trust,
            "likes":0,
            "reports":0,
            "time":datetime.now().strftime("%Y-%m-%d %H:%M"),
            "reasons":reasons

        })

        st.success("投稿しました！")

# -------------------------
# ランキング
# -------------------------

st.subheader("🏆 信頼度ランキング")

ranking = sorted(
    st.session_state.posts,
    key=lambda x:x["trust"],
    reverse=True
)

for i,p in enumerate(ranking[:3]):

    st.write(
        f"{i+1}位  {p['user']}  (信頼度 {p['trust']})"
    )

st.divider()

# -------------------------
# タイムライン
# -------------------------

st.subheader("📱 タイムライン")

posts = sorted(
    st.session_state.posts,
    key=lambda x:x["trust"],
    reverse=True
)

for i,post in enumerate(posts):

    st.markdown(
        '<div class="post-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### 👤 {post['user']}"
    )

    st.caption(post["time"])

    st.write(post["text"])

    trust = post["trust"]

    st.progress(trust)

    if trust >= 80:

        st.markdown(
            f'<p class="trust-high">🟢 信頼度 {trust}</p>',
            unsafe_allow_html=True
        )

    elif trust >= 60:

        st.markdown(
            f'<p class="trust-medium">🟡 信頼度 {trust}</p>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<p class="trust-low">🔴 信頼度 {trust}</p>',
            unsafe_allow_html=True
        )

        st.warning(
            "⚠ 未確認情報の可能性があります"
        )

    with st.expander("🤖 AI評価を見る"):

        if "reasons" in post:

            for r in post["reasons"]:
                st.write(r)

    col1,col2,col3 = st.columns(3)

    with col1:

        if st.button(
            f"👍 {post['likes']}",
            key=f"like{i}"
        ):
            post["likes"] += 1
            st.rerun()

    with col2:

        if st.button(
            f"🚨 {post['reports']}",
            key=f"report{i}"
        ):
            post["reports"] += 1
            st.rerun()

    with col3:

        st.write(f"🏆 #{i+1}")

    st.divider()
