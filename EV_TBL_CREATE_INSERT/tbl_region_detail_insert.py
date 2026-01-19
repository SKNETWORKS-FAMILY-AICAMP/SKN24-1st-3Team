import pandas as pd
import mysql.connector

# CSV 읽기
df = pd.read_csv('C:/SKN24/SKN24-1st-3Team/ev_region_detail.csv')
df.columns = df.columns.str.strip()  # 컬럼 공백 제거

# MySQL 연결
conn = mysql.connector.connect(
    host='localhost',
    user='ohgiraffers',
    password='ohgiraffers',
    database='evdb'
)
cursor = conn.cursor()

# INSERT
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO tbl_region_detail (zscode, regionDetailNm, zcode)
        VALUES (%s, %s, %s)
    """, (
        str(row['zscode']).strip(),            # zscode
        row['detail_regionNm'].strip(),        # CSV 컬럼명 → MySQL 컬럼 regionDetailNm
        str(row['zcode']).strip()              # zcode
    ))

conn.commit()
cursor.close()
conn.close()