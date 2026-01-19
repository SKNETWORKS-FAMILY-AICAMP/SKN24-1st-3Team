import streamlit as st
import pandas as pd
import pydeck as pdk
import pymysql

# 1. DB 연결 설정

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='ohgiraffers',
        password='ohgiraffers',
        db='evdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@st.cache_data # 데이터를 메모리에 저장해두어 앱 속도를 높임 (매번 DB에 새로 접속하지 않음)
def load_station_data():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # tbl_station에서 필요한 컬럼만 조회
            query = "SELECT statid, statNm, addr, lat, lng, parkingFree FROM tbl_station"
            cursor.execute(query)
            df_station = pd.DataFrame(cursor.fetchall())
            
            # 위도 경도의 결측치 가능성 제거
            if not df_station.empty:
                # 숫자형으로 변환 (오류 데이터는 NaN 처리)
                df_station['lat'] = pd.to_numeric(df_station['lat'], errors='coerce')
                df_station['lng'] = pd.to_numeric(df_station['lng'], errors='coerce')
                
                # 좌표가 없는 행은 지도 표시가 불가능하므로 삭제
                df_station = df_station.dropna(subset=['lat', 'lng'])
                
                # 주차 무료 여부 텍스트 변환
                df_station['parkingFree2'] = df_station['parkingFree'].map({'Y': '가능', 'N': '불가능'}).fillna('정보없음')
            
        return df_station
    finally:
        conn.close()


# 2. 데이터 로딩

df_stations = load_station_data()

st.title("전국 전기차 충전소 지도")

if df_stations.empty:
    st.warning("데이터베이스에서 불러온 충전소 데이터가 없습니다.")
else:
    st.write(f"총 충전소 개수: {len(df_stations)}")


    # 3. pydeck 레이어 설정

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_stations,
        get_position='[lng, lat]',    # pydeck은 [경도, 위도] 순서
        get_radius=40,               # 점 반경 조절
        get_fill_color=[65, 105, 225, 120], # RoyalBlue 색상
        pickable=True
    )


    # 4. 지도 뷰 설정

    view_state = pdk.ViewState(
        latitude=df_stations['lat'].mean(),
        longitude=df_stations['lng'].mean(),
        zoom=6
    )


    # 5. Streamlit에 지도 표시

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='road',
        tooltip={
            "html": "<b>충전소명:</b> {statNm}<br/><b>주소:</b> {addr}<br/><b>주차무료여부:</b> {parkingFree2}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    ))