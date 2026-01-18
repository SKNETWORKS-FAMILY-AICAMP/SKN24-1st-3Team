import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'ohgiraffers',
    password = 'ohgiraffers',
    database = 'evdb'
)

cursor = connection.cursor()

csv_path = r"C:\SKN24\EV_CRAWLING\ev_chargers_data (2).csv"   # 로컬에서의 csv 파일 경로
df = pd.read_csv(csv_path, encoding='utf-8-sig')      # 파일 읽기




### tbl_region 테이블에 데이터 적재 코드

# zcode의 unique 값만 추출
df_tbl_region = df[['zcode']].drop_duplicates()      # 중복값 제거

print(df_tbl_region)      # zcode가 처음 등장한 행이 인덱스로 출력
print(len(df_tbl_region))   # 길이 17

# zode와 지역 매핑
zcode_region_map = {
    '11': '서울',
    '26': '부산',
    '27': '대구',
    '28': '인천',
    '29': '광주',
    '30': '대전',
    '31': '울산',
    '36': '세종',
    '41': '경기',
    '43': '충북',
    '44': '충남',
    '46': '전남',
    '47': '경북',
    '48': '경남',
    '50': '제주',
    '51': '강원',
    '52': '전북'
}

# zcode 타입 맞추기 (CHAR(2)) --> 데이터타입을 문자열로 변환
df_tbl_region['zcode'] = df_tbl_region['zcode'].astype(str)

insert_sql = """
INSERT INTO tbl_region (zcode, regionNm)
VALUES (%s, %s)
"""

data_to_insert = []

for _, row in df_tbl_region.iterrows():     # df_tbl_region의 각 행을 하나씩 처리
    zcode = row['zcode']     # row는 시리즈, interrows()는 데이터프레임의 각 행을 하나씩 반환 -> 반환형식 (인덱스, 행데이터) 여기서 행데이터가 pandas.Series

    if zcode in zcode_region_map:    # 딕셔너리에서 in 연산자는 키가 있는지 확인
        regionNm = zcode_region_map[zcode]     # 해당 키에 연결된 값  가져옴
        data_to_insert.append((zcode, regionNm))
    else:
        print(f"[매핑 없음] zcode = {zcode}")

# 실제 INSERT 실행
cursor.executemany(insert_sql, data_to_insert)  # executemany -> 반복문 없이 여러 행 한 번에 삽입 가능
connection.commit()

print(f"tbl_region 적재 완료: {len(data_to_insert)}건")






### tbl_charger 테이블에 데이터 적재 코드

# 충전소 테이블에 필요한 컬럼만 선택
df_charger = df[[
    'statId',
    'statNm',
    'addr',
    'lat',
    'lng',
    'parkingFree',
    'limitYn',
    'limitDetail',
    'zscode'
]].copy()

#  충전소 기준 중복 제거
df_charger = df_charger.drop_duplicates(subset=['statId'])

# NaN → None (MySQL NULL 처리)
df_charger = df_charger.where(pd.notnull(df_charger), None)

# 타입 맞추기 (DB 스키마 기준)
df_charger['statId'] = df_charger['statId'].astype(str)
df_charger['zscode'] = df_charger['zscode'].astype(str)

# INSERT SQL
insert_sql = """
INSERT INTO tbl_charger
(
    statid,
    statNm,
    addr,
    lat,
    lng,
    parkingFree,
    limitYn,
    limitDetail,
    zscode
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# INSERT 데이터 구성
data_to_insert = []

for _, row in df_charger.iterrows():
    data_to_insert.append((
        row['statId'],
        row['statNm'],
        row['addr'],
        row['lat'],
        row['lng'],
        row['parkingFree'],
        row['limitYn'],
        row['limitDetail'],
        row['zscode']
    ))

# DB 적재
cursor.executemany(insert_sql, data_to_insert)
connection.commit()

print(f"tbl_charger 적재 완료: {len(data_to_insert)}건")

# 종료
cursor.close()
connection.close()
