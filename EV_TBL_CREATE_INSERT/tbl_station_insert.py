### tbl_staion 테이블에 데이터 적재 코드


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
INSERT INTO tbl_station
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


# 종료
cursor.close()
connection.close()