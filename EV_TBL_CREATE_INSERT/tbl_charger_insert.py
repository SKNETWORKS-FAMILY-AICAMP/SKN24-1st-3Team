import pandas as pd
import mysql.connector

# 1. DB 연결
conn = mysql.connector.connect(
    host="localhost",
    user="ohgiraffers",
    password="ohgiraffers",
    database="evdb"
)
cursor = conn.cursor()

# 2. CSV 로드
csv_path = r"C:\SKN24\EV_CRAWLING\ev_chargers_data (2).csv"
df = pd.read_csv(csv_path)

# 3. 필요한 컬럼만 추출 (CSV 기준)
df = df[
    [
        "statId",
        "chgerId",
        "chgerType",
        "stat",
        "output",
        "method",
        "year",
        "floorNum",
        "floorType",
        "useTime"
    ]
]

# 4. 타입 / 공백 정리
df["statId"] = df["statId"].astype(str).str.strip()
df["chgerId"] = df["chgerId"].astype(str).str.zfill(2)
df["chgerType"] = df["chgerType"].astype(str).str.strip()
df["method"] = df["method"].astype(str).str.strip()
df["useTime"] = df["useTime"].astype(str).str.strip()
df["floorType"] = df["floorType"].astype(str).str.strip()

df["stat"] = pd.to_numeric(df["stat"], errors="coerce")
df["output"] = pd.to_numeric(df["output"], errors="coerce")
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["floorNum"] = pd.to_numeric(df["floorNum"], errors="coerce")

df = df.dropna()  # 필수 컬럼 NULL 제거

# 5. 외래키 체크 (tbl_station에 없는 statId 제거)
cursor.execute("SELECT statId FROM tbl_station")
valid_stat_ids = {row[0] for row in cursor.fetchall()}

df = df[df["statId"].isin(valid_stat_ids)]

# 6. INSERT SQL
insert_sql = """
INSERT INTO tbl_charger
(statId, chgerId, chgerType, stat, output, method, install_year, floorNum, floorType, useTime)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    stat = VALUES(stat),
    output = VALUES(output),
    method = VALUES(method),
    install_year = VALUES(install_year),
    floorNum = VALUES(floorNum),
    floorType = VALUES(floorType),
    useTime = VALUES(useTime)
"""

# 7. 데이터 변환
data = [
    (
        row.statId,
        row.chgerId,
        row.chgerType,
        int(row.stat),
        int(row.output),
        row.method,
        int(row.year),
        int(row.floorNum),
        row.floorType,
        row.useTime
    )
    for row in df.itertuples(index=False)
]

# 8. 실행
cursor.executemany(insert_sql, data)
conn.commit()

print(f"✅ tbl_charger 적재 완료: {len(data)} rows")

cursor.close()
conn.close()
