import pathlib

import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# 기본 페이지 설정
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="돈포겟 · 실험 스케줄 관리",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 여백/헤더를 최소화해서 index.html이 화면을 최대한 채우도록 함
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] > .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }
        header[data-testid="stHeader"] {
            height: 0rem;
        }
        [data-testid="stToolbar"] {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# index.html 로드 & 렌더링
# ---------------------------------------------------------------------------
HTML_PATH = pathlib.Path(__file__).parent / "index.html"

if not HTML_PATH.exists():
    st.error(
        "index.html 파일을 찾을 수 없어요. app.py와 같은 폴더에 index.html을 함께 커밋했는지 확인해주세요."
    )
else:
    html_content = HTML_PATH.read_text(encoding="utf-8")

    # 화면 전체를 채우는 느낌으로: 넉넉한 고정 높이 + 내부 스크롤(index.html 내부 CSS가 처리)
    components.html(
        html_content,
        height=1400,
        scrolling=True,
    )

# ---------------------------------------------------------------------------
# 참고: Firebase 실시간 동기화
# ---------------------------------------------------------------------------
# index.html 안의 FIREBASE_CONFIG 값(apiKey, authDomain, databaseURL, projectId)이
# 현재 "REPLACE_ME"로 되어 있어요. Firebase 콘솔(console.firebase.google.com)에서
# 프로젝트를 만든 뒤 해당 값들을 index.html의 FIREBASE_CONFIG에 직접 채워 넣으면
# 여러 사용자 간 실시간 동기화가 활성화됩니다. (이 자리는 나중에 직접 설정하도록
# 비워둔 상태이며, 이 파일에서는 별도로 손대지 않았습니다.)
