import streamlit as st
from datetime import datetime
import hashlib

# =========================
# 信頼度スコアSNS
# Python + Streamlit
# =========================

st.set_page_config(
    page_title="信頼度スコアSNS",
    page_icon="🛡️",
    layout="wide",
)

# --- デザイン ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111a2e 55%, #101827 100%);
        color: #f4f7fb;
    }
    .block-container { padding-top: 2rem; max-width: 1200px; }
    h1, h2, h3 { color: #f4f7fb !important; }
    .hero {
        padding: 1.5rem 1.7rem;
        border: 1px solid rgba(125, 170, 255, .25);
        border-radius: 22px;
        background: linear-gradient(120deg, rgba(43, 83, 150, .32), rgba(20, 30, 52, .72));
        margin-bottom: 1.2rem;
    }
    .hero-sub { color: #b7c7e6; font-size: 1rem; }
    .post-card {
        border: 1px solid rgba(148, 170, 205, .22);
        border-radius: 18px;
        padding: 1rem 1.15rem;
        margin: .6rem 0 1rem 0;
        background: rgba(19, 29, 49, .88);
        box-shadow: 0 8px 24px rgba(0,0,0,.12);
    }
    .post-author { color: #9fc0ff; font-weight: 700; }
    .post-time { color: #8d9bb5; font-size: .8rem; }
    .post-text { color: #f3f6fc; font-size: 1.03rem; line-height: 1.65; margin: .7rem 0; }
    .score-pill {
        display: inline-block; padding: .28rem .65rem; border-radius: 999px;
        font-size: .85rem; font-weight: 700; margin-top: .3rem;
    }
    .score-high { background: rgba(42, 190, 130, .16); color: #73e4b4; border: 1px solid rgba(42,190,130,.3); }
    .score-mid { background: rgba(245, 183, 67, .15); color: #ffd27a; border: 1px solid rgba(245,183,67,.3); }
    .score-low { background: rgba(255, 105, 105, .14); color: #ff9d9d; border: 1px solid rgba(255,105,105,.3); }
    .small-note { color: #9aa9c2; font-size: .82rem; }
    [data-testid="stMetric"] {
        background: rgba(24, 38, 63, .75);
        border: 1px solid rgba(148, 170, 205, .18);
        padding: .8rem 1rem;
        border-radius: 14px;
    }
    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(125,170,255,.35);
    }
</style>
""", unsafe_allow_html=True)

# --- 信頼度スコア（試作） ---
POSITIVE_WORDS = {
    "出典": 8, "証拠": 8, "研究": 6, "論文": 8,
    "統計": 7, "データ": 5, "公式": 6, "一次資料": 8,
}
NEGATIVE_WORDS = {
    "絶対": 8, "100%": 10, "必ず": 7, "確実": 6,
    "噂": 8, "拡散希望": 5, "秘密": 4, "絶対に": 8,
}

def calculate_trust(text):
    score = 50
    reasons = []
    for word, points in POSITIVE_WORDS.items():
        if word in text:
            score += points
            reasons.append(f"「{word}」を含むため +{points}")
    for word, points in NEGATIVE_WORDS.items():
        if word in text:
            score -= points
            reasons.append(f"「{word}」を含むため -{points}")
    score = max(0, min(100, score))
    if not reasons:
        reasons.append("判定対象のキーワードが見つからないため、基準点50")
    return score, reasons

def score_label(score):
    if score >= 70:
        return "比較的高い", "score-high"
    if score >= 40:
        return "要確認", "score-mid"
    return "注意が必要", "score-low"

def make_post(author, text, time_label, likes=0, source="サンプル投稿"):
    score, reasons = calculate_trust(text)
    post_id = hashlib.sha1(f"{author}|{text}|{time_label}".encode("utf-8")).hexdigest()[:10]
    return {
        "id": post_id,
        "author": author,
        "text": text,
        "time": time_label,
        "likes": likes,
        "liked": False,
        "trust": score,
        "reasons": reasons,
        "source": source,
    }

# --- 最初から表示するサンプル投稿10件 ---
def initial_posts():
    samples = [
        ("情報メモ", "気象情報を確認するときは、気象庁の公式発表や出典を確認しよう。", "10分前", 12),
        ("理科好き", "研究結果を紹介するときは、元の論文や調査方法も読むことが大切。", "18分前", 8),
        ("データ部", "統計データを見るときは、対象人数や調査した時期も確認したい。", "25分前", 15),
        ("みんなの話題", "これ絶対本当らしい！詳しい出典はまだ見つかっていないけど、拡散希望！", "32分前", 27),
        ("ニュース確認係", "ニュースを見たら、公式発表と複数の報道機関の情報を比べてみよう。", "40分前", 19),
        ("うわさ発見", "友達から聞いた噂だけど、明日から学校のルールが全部変わるらしい。", "48分前", 6),
        ("読書ノート", "専門家の説明を読むときも、どんな証拠やデータが示されているか確認しよう。", "55分前", 10),
        ("速報ウォッチ", "100%確実な情報です！今すぐ信じて、必ず周りにも知らせてください。", "1時間前", 31),
        ("学びの共有", "情報の投稿日を確認すると、古い情報を現在の出来事と誤解するのを防げる。", "1時間前", 14),
        ("調べてみた", "ある投稿を見かけたけれど、一次資料が見つからなかったので、まだ判断を保留中。", "2時間前", 9),
    ]
    return [make_post(a, t, tm, likes) for a, t, tm, likes in samples]

if "posts" not in st.session_state:
    st.session_state.posts = initial_posts()
if "liked_ids" not in st.session_state:
    st.session_state.liked_ids = set()

# --- ヘッダー ---
st.markdown("""
<div class="hero">
  <div style="font-size:.85rem; letter-spacing:.14em; color:#8fb6ff;">TRUST SCORE SOCIAL</div>
  <h1 style="margin:.35rem 0 .4rem 0;">🛡️ 信頼度スコアSNS</h1>
  <div class="hero-sub">情報をすぐに信じるのではなく、根拠を確認するきっかけをつくるSNS</div>
</div>
""", unsafe_allow_html=True)

st.caption("※ 最初に表示される10件はデモ用の架空投稿です。実在のニュースや事実を示すものではありません。")

# --- サマリー ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("投稿数", f"{len(st.session_state.posts)} 件")
with col2:
    avg = round(sum(p["trust"] for p in st.session_state.posts) / max(1, len(st.session_state.posts)))
    st.metric("平均スコア", f"{avg} / 100")
with col3:
    st.metric("いいね合計", f"{sum(p['likes'] for p in st.session_state.posts)}")

st.divider()

# --- サイドバー：投稿フォームと説明 ---
with st.sidebar:
    st.header("✍️ 新しい投稿")
    with st.form("new_post_form", clear_on_submit=True):
        author = st.text_input("表示名", value="ゲスト")
        post_text = st.text_area("投稿内容", placeholder="情報の根拠や出典も書いてみよう…", height=140)
        submitted = st.form_submit_button("投稿する", use_container_width=True)
        if submitted:
            if not author.strip() or not post_text.strip():
                st.warning("表示名と投稿内容を入力してください。")
            else:
                now = datetime.now().strftime("%H:%M")
                st.session_state.posts.insert(
                    0, make_post(author.strip(), post_text.strip(), f"今日 {now}", 0, "ユーザー投稿")
                )
                st.success("投稿しました！")
                st.rerun()

    st.divider()
    st.subheader("スコアの見方")
    st.markdown("""
    - 🟢 **70〜100点**：比較的高い
    - 🟡 **40〜69点**：要確認
    - 🔴 **0〜39点**：注意が必要
    """)
    st.markdown('<div class="small-note">このスコアはキーワードに基づく簡易的な試作です。正確性を保証するものではありません。</div>', unsafe_allow_html=True)

# --- タイムライン ---
left, right = st.columns([3, 1])
with left:
    st.subheader("📰 タイムライン")
with right:
    sort_mode = st.selectbox("並び順", ["信頼度が高い順", "新しい投稿順", "いいねが多い順"], label_visibility="collapsed")

posts = list(st.session_state.posts)
if sort_mode == "信頼度が高い順":
    posts.sort(key=lambda p: p.get("trust", 50), reverse=True)
elif sort_mode == "いいねが多い順":
    posts.sort(key=lambda p: p.get("likes", 0), reverse=True)

for post in posts:
    score = post.get("trust", calculate_trust(post.get("text", ""))[0])
    label, css_class = score_label(score)
    st.markdown(f"""
    <div class="post-card">
      <div style="display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
        <div class="post-author">👤 {post.get('author', 'ゲスト')}</div>
        <div class="post-time">{post.get('time', '')}</div>
      </div>
      <div class="post-text">{post.get('text', '')}</div>
      <span class="score-pill {css_class}">信頼度スコア：{score}/100 · {label}</span>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("スコアの理由を見る"):
        reasons = post.get("reasons")
        if not reasons:
            _, reasons = calculate_trust(post.get("text", ""))
        for reason in reasons:
            st.write(f"• {reason}")
        st.caption("キーワードだけでは、情報が正しいかどうかは判定できません。出典や根拠を自分でも確認してください。")

    liked = post.get("id") in st.session_state.liked_ids
    button_label = f"❤️ いいね済み（{post.get('likes', 0)}）" if liked else f"🤍 いいね（{post.get('likes', 0)}）"
    if st.button(button_label, key=f"like_{post.get('id')}", disabled=liked):
        post["likes"] = post.get("likes", 0) + 1
        st.session_state.liked_ids.add(post.get("id"))
        st.rerun()

st.divider()
st.markdown("### 🔬 探究のポイント")
st.write("このアプリは、投稿文に含まれるキーワードで仮のスコアを計算する試作品です。今後は、スコア表示の有無で人の信頼判断や共有したい気持ちが変化するかを比較すると、研究としてさらに深められます。")
