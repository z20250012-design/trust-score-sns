import streamlit as st

st.set_page_config(page_title='信頼度スコアSNS')

st.title('🛡️ 信頼度スコアSNS')

def calc_score(source,multi,ai,anonymous):
    score=0
    if source: score+=40
    if multi: score+=30
    if ai: score+=20
    if anonymous: score-=30
    return max(0,min(score,100))

with st.sidebar:
    text=st.text_area('投稿内容')
    source=st.checkbox('情報源あり')
    multi=st.checkbox('複数ソース確認')
    ai=st.checkbox('AI確認済み')
    anonymous=st.checkbox('匿名投稿')

    if st.button('投稿'):
        if 'posts' not in st.session_state:
            st.session_state.posts=[]
        st.session_state.posts.append({
            'text':text,
            'score':calc_score(source,multi,ai,anonymous)
        })

if 'posts' not in st.session_state:
    st.session_state.posts=[
        {'text':'札幌で大雪警報が発表','score':90},
        {'text':'学校が休校になるらしい','score':40},
        {'text':'有名人が宇宙人だったらしい','score':20}
    ]

for p in sorted(st.session_state.posts,key=lambda x:x['score'],reverse=True):
    st.write(f"信頼度 {p['score']}/100")
    st.write(p['text'])
    st.divider()
