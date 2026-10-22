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
    .score-low {
        background: #fff0ef;
        color: #a12d2d;
        border: 1px solid #f3cecb;
    }
    .small-note {
        color: #68758b;
        font-size: .82rem;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e7f0;
        padding: .85rem 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 14px rgba(24,44,80,.035);
    }
    div.stButton > button, div.stFormSubmitButton > button {
        border-radius: 11px;
        border: 1px solid #d4deed;
    }
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #245fc7;
        color: white;
        border-color: #245fc7;
    }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e1e7f0;
    }
    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #e1e7f0;
        border-radius: 12px;
    }
    .section-caption {
        color: #6a7890;
        font-size: .9rem;
    }
</style>
""", unsafe_allow_html=True)

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
        reasons.append("判定対象のキーワードがないため、基準点50")
    return score, reasons

def score_label(score):
    if score >= 70:
        return "比較的高い", "score-high"
    if score >= 40:
        return "要確認", "score-mid"
    return "注意が必要", "score-low"

def make_post(author, text, time_label, likes=0, source="サンプル投稿"):
    score, reasons = calculate_trust(text)
    return {
        "id": str(uuid.uuid4()),
        "author": author,
        "text": text,
        "time": time_label,
        "likes": likes,
        "trust": score,
        "reasons": reasons,
        "source": source,
    }

def initial_posts():
    # デモ投稿はこの関数で10件まとめて作成する
    samples = [
        ("情報メモ", "気象情報を確認するときは、気象庁などの公式発表や出典を確認しよう。", "10分前", 12),
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
    return [make_post(a, text, tm, likes) for a, text, tm, likes in samples]

# 初回起動時だけ10件を作る。再読み込みで1件に戻さない。
if "posts" not in st.session_state:
    st.session_state.posts = initial_posts()
else:
    # 以前の版で投稿データが古い形式でも表示できるように補正
    fixed_posts = []
    for old in st.session_state.posts:
        if not isinstance(old, dict):
            continue
        text = str(old.get("text", ""))
        score, reasons = calculate_trust(text)
        old.setdefault("id", str(uuid.uuid4()))
        old.setdefault("author", "ゲスト")
        old.setdefault("time", "")
        old.setdefault("likes", 0)
        old.setdefault("trust", score)
        old.setdefault("reasons", reasons)
        fixed_posts.append(old)
    st.session_state.posts = fixed_posts
    # 以前のコードで空・1件だけの状態で起動していた場合は、
    # 初期サンプル10件を追加してタイムラインを充実させる。
    if len(st.session_state.posts) < 10:
        existing_texts = {p.get("text", "") for p in st.session_state.posts}
        for sample in initial_posts():
            if sample["text"] not in existing_texts:
                st.session_state.posts.append(sample)
                existing_texts.add(sample["text"])
            if len(st.session_state.posts) >= 10:
                break

st.title("🛡️ 信頼度スコアSNS")
st.markdown(
    '<div class="hero"><div class="hero-kicker">TRUST SCORE SOCIAL</div>'
    '<div class="hero-title">情報を、確かめてから共有しよう。</div>'
    '<div class="hero-sub">投稿の特徴をもとに簡易スコアを表示し、情報を確認するきっかけをつくるSNSの試作品です。</div></div>',
    unsafe_allow_html=True,
)
st.caption("最初に表示されるサンプル投稿はデモ用の架空投稿です。実在のニュースや事実を示すものではありません。")

total_posts = len(st.session_state.posts)
avg_score = round(sum(p.get("trust", 50) for p in st.session_state.posts) / max(total_posts, 1))
total_likes = sum(p.get("likes", 0) for p in st.session_state.posts)

m1, m2, m3 = st.columns(3)
m1.metric("投稿数", f"{total_posts} 件")
m2.metric("平均スコア", f"{avg_score} / 100")
m3.metric("いいね合計", f"{total_likes}")

with st.sidebar:
    st.header("✍️ 新しい投稿")
    with st.form("new_post_form", clear_on_submit=True):
        author = st.text_input("表示名", value="ゲスト")
        text = st.text_area("投稿内容", placeholder="投稿内容を入力してください…", height=130)
        submit = st.form_submit_button("投稿する", use_container_width=True)
    if submit:
        if author.strip() and text.strip():
            st.session_state.posts.insert(
                0, make_post(author.strip(), text.strip(), f"今日 {datetime.now().strftime('%H:%M')}", 0, "ユーザー投稿")
            )
            st.success("投稿しました！")
            st.rerun()
        else:
            st.warning("表示名と投稿内容を入力してください。")

    st.divider()
    st.subheader("スコアの見方")
    st.markdown("🟢 **70〜100点**：比較的高い  \n🟡 **40〜69点**：要確認  \n🔴 **0〜39点**：注意が必要")
    st.markdown('<div class="small-note">スコアはキーワードによる試作判定です。点数だけで情報の真偽を断定することはできません。</div>', unsafe_allow_html=True)

feed_col, sort_col = st.columns([3, 1])
with feed_col:
    st.subheader("📰 タイムライン")
    st.markdown('<div class="section-caption">投稿を開いて、スコアの理由も確認できます。</div>', unsafe_allow_html=True)
with sort_col:
    sort_mode = st.selectbox("並び順", ["信頼度が高い順", "新しい投稿順", "いいねが多い順"])

posts = list(st.session_state.posts)
if sort_mode == "信頼度が高い順":
    posts.sort(key=lambda p: p.get("trust", 50), reverse=True)
elif sort_mode == "いいねが多い順":
    posts.sort(key=lambda p: p.get("likes", 0), reverse=True)

for post in posts:
    score = post.get("trust", calculate_trust(post.get("text", ""))[0])
    label, css_class = score_label(score)
    author_safe = html.escape(str(post.get("author", "ゲスト")))
    text_safe = html.escape(str(post.get("text", ""))).replace("\n", "<br>")
    time_safe = html.escape(str(post.get("time", "")))
    st.markdown(
        f'<div class="post-card"><div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;">'
        f'<div class="post-author">👤 {author_safe}</div><div class="post-time">{time_safe}</div></div>'
        f'<div class="post-text">{text_safe}</div>'
        f'<span class="score-pill {css_class}">信頼度スコア：{score}/100 · {label}</span></div>',
        unsafe_allow_html=True,
    )
    with st.expander("スコアの理由を見る"):
        reasons = post.get("reasons")
        if not reasons:
            _, reasons = calculate_trust(post.get("text", ""))
        for reason in reasons:
            st.write(f"• {reason}")
        st.caption("キーワードの有無だけでは正しさを判断できません。出典や根拠を自分でも確認しましょう。")
    if st.button(f"🤍 いいね（{post.get('likes', 0)}）", key=f"like_{post['id']}"):
        post["likes"] = post.get("likes", 0) + 1
        st.rerun()

st.divider()
st.subheader("🔬 探究のポイント")
st.write("この試作品では、投稿文のキーワードを使って仮のスコアを計算しています。今後は、スコア表示の有無で人の信頼判断や共有したい気持ちが変化するかを比較すると、探究をさらに深められます。")
