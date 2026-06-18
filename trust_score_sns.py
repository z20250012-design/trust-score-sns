import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="信頼度スコアSNS Ver.7",
    page_icon="🛡️",
    layout="wide"
)

# ----------------------------
# 初期化
# ----------------------------

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

# ----------------------------
# 信頼度計算
# ----------------------------

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

    reasons = []

    for word in positive_words:

        if word in text:

            score += 8
            reasons.append(f"✓ {word}")

    for word in negative_words:

        if word in text:

            score -= 8
            reasons.append(f"⚠ {word}")

    score = max(0,min(score,100))

    return score,reasons

# ----------------------------
# サイドバー
# ----------------------------

with st.sidebar:

    st.title("🛡️ メニュー")

    page = st.radio(
        "ページ選択",
        ["📱タイムライン","📊分析"]
    )

    st.divider()

    username = st.text_input(
        "ユーザー名",
        value="匿名ユーザー"
    )

# ----------------------------
# タイムライン
# ----------------------------

if page == "📱タイムライン":

    st.title("🛡️ 信頼度スコアSNS")

    st.caption(
        "信頼度の高い投稿ほど上に表示"
    )

    st.subheader("✏️ 投稿")

    post_text = st.text_area(
        "投稿内容"
    )

    if st.button("投稿する"):

        if post_text.strip():

            trust,reasons = calculate_trust(
                post_text
            )

            st.session_state.posts.append({

                "user":username,
                "text":post_text,
                "trust":trust,
                "likes":0,
                "reports":0,
                "reasons":reasons,
                "time":datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )

            })

            st.success("投稿しました")

    st.divider()

    sort_option = st.selectbox(
        "並び替え",
        [
            "信頼度順",
            "新着順",
            "いいね順"
        ]
    )

    if sort_option == "信頼度順":

        posts = sorted(
            st.session_state.posts,
            key=lambda x:x["trust"],
            reverse=True
        )

    elif sort_option == "いいね順":

        posts = sorted(
            st.session_state.posts,
            key=lambda x:x["likes"],
            reverse=True
        )

    else:

        posts = list(
            reversed(
                st.session_state.posts
            )
        )

    st.subheader("📱 タイムライン")

    for i,post in enumerate(posts):

        with st.container():

            st.markdown(
                f"### 👤 {post['user']}"
            )

            st.caption(post["time"])

            st.write(post["text"])

            trust = post["trust"]

            st.progress(trust)

            if trust >= 80:

                st.success(
                    f"🟢 信頼度 {trust}"
                )

            elif trust >= 60:

                st.info(
                    f"🟡 信頼度 {trust}"
                )

            else:

                st.error(
                    f"🔴 信頼度 {trust}"
                )

                st.warning(
                    "⚠ 注意ラベル: 未確認情報の可能性があります"
                )

            with st.expander(
                "🤖 AI評価理由"
            ):

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

                st.write(
                    f"🏆 #{i+1}"
                )

            st.divider()

# ----------------------------
# 分析ページ
# ----------------------------

else:

    st.title("📊 分析ダッシュボード")

    df = pd.DataFrame(
        st.session_state.posts
    )

    total_posts = len(df)

    avg_trust = round(
        df["trust"].mean(),
        1
    )

    high_ratio = round(
        (df["trust"] >= 80).mean()*100,
        1
    )

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "投稿数",
        total_posts
    )

    c2.metric(
        "平均信頼度",
        avg_trust
    )

    c3.metric(
        "高信頼投稿割合",
        f"{high_ratio}%"
    )

    st.divider()

    st.subheader(
        "📈 信頼度分布"
    )

    fig = px.histogram(
        df,
        x="trust",
        nbins=10
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "🚨 通報数ランキング"
    )

    top_reports = df.sort_values(
        "reports",
        ascending=False
    )

    fig2 = px.bar(
        top_reports.head(10),
        x="user",
        y="reports"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
