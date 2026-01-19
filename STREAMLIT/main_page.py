# app.py
import streamlit as st

st.set_page_config(
    page_title="EV 데이터 통합 대시보드",
    layout="wide"
)

st.title("🚗 전기차 현황 통합 대시보드")

st.markdown("""
### 프로젝트 개요
본 대시보드는 국내 전기차 등록 현황과 충전 인프라 데이터를
통합 분석하기 위해 제작되었습니다.

⬅️ 왼쪽 사이드바에서 원하는 분석 페이지를 선택하세요.
""")

st.info("팀원별로 분석한 결과를 하나의 Streamlit 대시보드로 통합했습니다.")
