import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="信頼度スコアSNS",
    page_icon="🛡️"
)

st.title("🛡️ 信頼度スコアSNS")
st.caption("信頼度の高い情報を見つけやすくするSNS")

# --------------------
# 初期化
# --------------------

if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "user": "運営",
            "text": "ようこそ！これは探究用SNSです。",
            "trust": 100,
            "likes": 0,
            "reports": 0,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]

# --------------------
# 信頼度計算
# --------------------

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

    score = max(0, min(score, 100))

    return score

# --------------------
# ユーザー設定
# --------------------

with st.sidebar:

    st.header("👤 ユーザー")

    username = st.text_input(
        "名前",
        value="匿名ユーザー"
    )

# --------------------
# 投稿
# --------------------

st.subheader("✏️ 投稿")

post_text = st.text_area("内容を入力")

if st.button("投稿する"):

    if post_text.strip():

        trust = calculate_trust(post_text)

        st.session_state.posts.append({
            "user": username,
            "text": post_text,
            "trust": trust,
            "likes": 0,
            "reports": 0,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        st.success("投稿しました！")

# --------------------
# タイムライン
# --------------------

st.subheader("📱 タイムライン")

sorted_posts = sorted(
    st.session_state.posts,
    key=lambda x: x.get("trust", 0),
    reverse=True
)

for i, post in enumerate(sorted_posts):

    st.markdown(f"### 👤 {post['user']}")

    st.caption(post["time"])

    st.write(post["text"])

    trust = post.get("trust", 0)

    st.progress(trust)

    if trust >= 80:
        st.success(f"🟢 信頼度 {trust}")
    elif trust >= 60:
        st.info(f"🟡 信頼度 {trust}")
    else:
        st.error(f"🔴 信頼度 {trust}")

    if trust < 60:
        st.warning(
            "⚠ この投稿は未確認情報の可能性があります"
        )

    col1, col2, col3 = st.columns(3)

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
