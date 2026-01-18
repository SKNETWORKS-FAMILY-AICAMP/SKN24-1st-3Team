import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt #그림 그리는 도구
import matplotlib.ticker as ticker #그래프 축 다듬는 것

#웹사이트 기본 설정
st.set_page_config(
    page_title="전기차 등록 현황 대시보드", #제목
    page_icon="⚡", #제목 옆에 뜰 아이콘
    layout="wide"
)

plt.rc('font', family='Malgun Gothic')  #그래프 그릴 때 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False #숫자 앞에 마이너스 기호가 깨지는 걸 막는 코드 

@st.cache_data #한 번 가져온 데이터는 기억해둘 것

#데이터 로딩해주는 함수
def load_data():
    #데이터베이스로 연결하기
    conn = pymysql.connect(
        host="127.0.0.1",
        user="ohgiraffers",
        password="ohgiraffers",
        database="evdb",
        port=3306,
        charset="utf8mb4",
    )
    try:
        query = "SELECT year, region, registrations FROM tbl_region"
        #SQL 쿼리 작성
        df = pd.read_sql(query, conn) #쿼리대로 데이터를 가져와서 표로 만들기
        return df #만든 표 변환
    finally:
        conn.close() #실행 닫아주기

#UI

#사이드바 제작
with st.sidebar:
    st.header("📊 데이터 필터")
    st.write("확인하고 싶은 지역을 선택하세요.")

try:
    df = load_data()

    #데이터가 안 비어있으면
    if df is not None:
        region_list = sorted(df['region'].unique()) #지역 이름들만 중복 없이 뽑아서 정렬
        selected_region = st.selectbox("지역 선택", region_list) #선택 상자 만들고, 고른 지역 변수에 저장
        
        filtered_df = df[df['region'] == selected_region].sort_values('year') #내가 고른 지역만 남기고 연도순 정렬 

        st.title(f"⚡ {selected_region} 전기차 등록 추이 분석") #대제목
        st.markdown("---") #가로줄 그어서 구분

        #그 지역 데이터가 진짜 있으면?
        if not filtered_df.empty:
            
            last_row = filtered_df.iloc[-1]   #맨 마지막 줄 가져오기
            first_row = filtered_df.iloc[0]   #맨 첫 줄 가져오기
            
            col1, col2 = st.columns(2) #화면 2개로 분리

            #최근 등록 대수 보여주고 숫자에 쉼표 찍기
            with col1:
                st.metric("최근 등록 대수", f"{int(last_row['registrations']):,}대")
            
            #데이터 집계 기간 보여주고 몇 년부터 몇 년까지 보여주기
            with col2:
                st.metric("데이터 집계 기간", f"{int(first_row['year'])} ~ {int(last_row['year'])}")

            st.markdown("---")

            #좌표
            fig, ax = plt.subplots(figsize=(12, 7))
            
            #꺾은선그래프
            ax.plot(filtered_df['year'], filtered_df['registrations'], 
                    color='#3B82F6', marker='o', markersize=8, linewidth=3, zorder=2)
            
            #그래프 선 아래쪽 연한 파란색으로 색칠
            ax.fill_between(filtered_df['year'], filtered_df['registrations'], 
                            color='#3B82F6', alpha=0.1)

            #y축(세로축) 범위 잡기
            min_val = filtered_df['registrations'].min()
            max_val = filtered_df['registrations'].max()
            padding = (max_val - min_val) * 0.2 if max_val != min_val else 10
            ax.set_ylim(max(0, min_val - padding), max_val + padding)
            
            #세로축 1000씩 떨어지게
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
            ax.grid(True, linestyle='--', alpha=0.4, axis='y')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            #점 위에 숫자 쓰기
            for i, row in filtered_df.iterrows():
                ax.annotate(
                    text=f"{int(row['registrations']):,}", 
                    xy=(row['year'], row['registrations']), 
                    xytext=(0, 10),  #점 위로 10포인트 띄우기
                    textcoords='offset points', 
                    ha='center', 
                    va='bottom',
                    fontsize=12, 
                    fontweight='bold', 
                    color='#1E3A8A',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8)
                )

            ax.set_xlabel("연도", fontsize=12)
            ax.set_ylabel("등록 대수 (단위: 대)", fontsize=12)
            ax.set_xticks(filtered_df['year'])
            
            st.pyplot(fig)

            with st.expander("📄 상세 데이터 표 보기"):
                st.dataframe(filtered_df.style.format({"registrations": "{:,}대"}))
        
        #만약 데이터가 없으면?
        else:
          st.info("해당 지역의 데이터가 없습니다.")

   #만약 load_data에서 데이터를 못 가져왔으면?
    else:
        st.error("데이터 로드 실패") #실패했다.

#코드 실행했다가 에러 터지면
except Exception as e:
    st.error("오류 발생")
    st.write(f"내용: {e}")