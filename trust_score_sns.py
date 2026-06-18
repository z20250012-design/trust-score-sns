import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="信頼度スコアSNS",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ 信頼度スコアSNS")
st.caption("信頼度が高い投稿ほど上に表示されます")

if "posts" not in st.session_state:
    st.session_state.posts = []

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

with st.sidebar:

    st.header("👤 ユーザー")

    username = st.text_input(
        "名前",
        value="匿名ユーザー"
    )

st.subheader("✏️ 投稿")

post_text = st.text_area(
    "内容を書いてください"
)

if st.button("投稿する"):

    if post_text:

        trust = calculate_trust(post_text)

        st.session_state.posts.append({
            "user": username,
            "text": post_text,
            "trust": trust,
            "likes": 0,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

st.divider()

st.subheader("📱 タイムライン")

sorted_posts = sorted(
    st.session_state.posts,
    key=lambda x: x["trust"],
    reverse=True
)

for i, post in enumerate(sorted_posts):

    with st.container():

        st.markdown(
            f"### 👤 {post['user']}"
        )

        st.caption(post["time"])

        st.write(post["text"])

        trust = post["trust"]

        st.progress(trust)

        if trust >= 80:
            st.success(f"信頼度 {trust}点")
        elif trust >= 60:
            st.info(f"信頼度 {trust}点")
        else:
            st.error(f"信頼度 {trust}点")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                f"👍 {post['likes']}",
                key=f"like{i}"
            ):
                post["likes"] += 1
                st.rerun()

        with col2:
            st.write(
                f"🏆順位 #{i+1}"
            )

        st.divider()
