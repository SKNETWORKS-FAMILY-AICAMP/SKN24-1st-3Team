#0. pandas, pd 
import pandas as pd
import pymysql

#1. 원본 데이터 -> 로우데이터 현재 문자형이기 때문에 숫자로 바꿔줘야 함
raw_data = [
    ['2025', '87,135', '50,122', '34,515', '71,284', '16,277', '22,387', '12,485', '6,718', '166,319', '20,398', '25,862', '28,961', '22,764', '33,094', '29,951', '52,778', '47,302', '728,352'],
    ['2024', '74,116', '38,277', '28,868', '48,498', '13,051', '18,961', '9,951', '5,234', '124,529', '16,955', '20,054', '22,609', '18,717', '25,329', '22,134', '37,441', '39,059', '563,783'],
    ['2023', '64,369', '29,569', '24,479', '35,275', '10,682', '15,735', '8,196', '4,379', '92,771', '14,560', '15,393', '17,954', '14,581', '19,450', '16,805', '29,267', '30,568', '444,033'],
    ['2022', '53,612', '19,593', '20,210', '23,974', '8,025', '13,044', '6,301', '3,044', '66,606', '11,842', '12,316', '13,234', '9,901', '12,770', '12,555', '19,278', '25,736', '332,041'],
    ['2021', '37,617', '11,163', '13,942', '11,829', '4,961', '7,204', '4,727', '1,874', '34,642', '7,550', '6,778', '8,194', '5,888', '7,565', '7,779', '11,146', '21,325', '204,184'],
    ['2020', '17,463', '4,628', '9,014', '4,581', '3,041', '3,591', '3,552', '897', '16,116', '3,540', '3,160', '4,513', '2,586', '3,756', '4,246', '5,023', '12,338', '102,045'],
    ['2019', '9,796', '3,076', '8,467', '2,169', '2,329', '2,349', '2,421', '665', '9,131', '2,031', '2,052', '2,558', '1,401', '2,234', '2,930', '3,107', '11,064', '67,780'],
    ['2018', '4,745', '1,010', '4,393', '790', '1,084', '1,019', '909', '218', '3,876', '892', '812', '721', '616', '981', '1,018', '1,387', '8,088', '32,559'],
    ['2017', '1,191', '401', '568', '233', '197', '104', '184', '24', '729', '170', '100', '167', '139', '384', '258', '446', '3,255', '8,550'],
    ['2016', '785', '172', '119', '94', '105', '19', '30', '8', '236', '76', '21', '68', '18', '221', '102', '303', '2,567', '4,944'],
    ['2015', '694', '142', '36', '77', '97', '13', '26', '7', '171', '61', '16', '62', '16', '188', '85', '299', '1,605', '3,595'],
    ['2014', '378', '67', '10', '49', '63', '10', '11', '2', '96', '32', '4', '44', '4', '78', '52', '188', '433', '1,521'],
    ['2013', '134', '9', '3', '13', '2', '7', '8', '2', '40', '10', '1', '27', '0', '15', '17', '82', '131', '501'],
    ['2012', '48', '7', '2', '10', '1', '2', '7', '0', '32', '7', '0', '3', '0', '10', '10', '51', '42', '232'],
    ['2011', '41', '4', '2', '7', '0', '2', '7', '0', '23', '5', '0', '1', '0', '7', '8', '51', '40', '198'],
    ['2010', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '5']
]

#2. 컬럼명: raw data에 각 위치에 이름을 붙여주기 위함
columns = [
    "year",
    "seoul", "busan", "daegu", "incheon", "gwangju", "daejeon", "ulsan", "sejong",
    "gyeonggi", "gangwon", "chungbuk", "chungnam", "jeonbuk", "jeonnam",
    "gyeongbuk", "gyeongnam", "jeju",
    "total"
]

#3. Dataframe 생성 + 전처리 (콤마 제거, 정수 변환)
df = pd.DataFrame(raw_data, columns=columns)

df["year"] = df["year"].astype(int) #year을 숫자로 변형해주는 과정

num_cols = df.columns.drop("year") #df.columns는 모든 컬럼 목록, year만 빼고 나머지(지역 + total)를 num_cols로 잡음

df[num_cols] = (
    df[num_cols]
    .replace(",", "", regex=True)    #'87,135' -> '87135'
    .astype(int)                     #문자열 -> int. 정수로 변환
)  

print(df.head()) #상위 5행 출력하기
print(df.dtypes) #year 포함 전부 int로 바뀌었는지 확인

#4. MySQL 접속 정보 (본인 환경으로 수정)
db_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "ohgiraffers",
    "password": "ohgiraffers",
    "database": "evdb",
    "charset": "utf8mb4",
    "autocommit": False,
}   #ohgiraffers 환경에 맞게 해줌

table_name = "tbl_register"

#5. MySQL 적재 (테이블 생성 + UPSERT)
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    year INT NOT NULL,
    seoul INT NOT NULL,
    busan INT NOT NULL,
    daegu INT NOT NULL,
    incheon INT NOT NULL,
    gwangju INT NOT NULL,
    daejeon INT NOT NULL,
    ulsan INT NOT NULL,
    sejong INT NOT NULL,
    gyeonggi INT NOT NULL,
    gangwon INT NOT NULL,
    chungbuk INT NOT NULL,
    chungnam INT NOT NULL,
    jeonbuk INT NOT NULL,
    jeonnam INT NOT NULL,
    gyeongbuk INT NOT NULL,
    gyeongnam INT NOT NULL,
    jeju INT NOT NULL,
    total INT NOT NULL,
    PRIMARY KEY (year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

#CREATE TABLE IF NOT EXISTS: 테이블이 없으면 만들고 있으면 그대로 둠
#int not null: null값 허용 안 함
#Primary Key를 year로 -> on duplicate key update가 실행

col_sql = ", ".join(columns) #컬럼명 문자열 만들기
placeholders = ", ".join(["%s"] * len(columns)) #placeholder 만들기: 컬럼 수만큼 %s를 만들어줌 -> pymysql에서 안전하게 값을 바인딩할 때 사용
update_assignments = ", ".join([f"{c}=VALUES({c})" for c in columns if c != "year"]) #업데이트 구문 만들기 -> year는 pk라서 업데이트하면 의미가 없으니 제외

insert_sql = f"""
INSERT INTO {table_name} ({col_sql})
VALUES ({placeholders})
ON DUPLICATE KEY UPDATE {update_assignments};
""" #year가 새 값이면 INSERT, year가 이미 있으면 Primary Key가 중복되기 때문에 Update로 덮어씀

#main() 함수: 실제 DB 작업 수행
def main():
    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cur:
            cur.execute(create_table_sql) #cursor: SQL실행 담당 객체, 테이블 생성 SQL 실행.

            #DataFrame: list[tuple] 변환 후 일괄 적재
            data_to_insert = [tuple(row) for row in df.to_numpy()] #각 행을 tuple로 바꿔서 (2025, 87135, 50122, ..., 728352) 형태로 바꿔줌
            cur.executemany(insert_sql, data_to_insert) #같은 SQL을 여러 행에 대해 반복 실행(배치 삽입) -> 행 개수만큼 Insert 시도. 중복 year는 update 처리

        conn.commit() #실제 저장 확정
        print(f"OK: {len(df)} rows upserted into evdb.{table_name}") #성공 메시지 출력

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)
        raise
    finally:
        conn.close()

    #예외처리: 오류가 나면 rollback()으로 이번 작업 전부 취소 -> DB에 반영 X
    #에러 메시지 출력 후 raise로 예외를 다시 던져서 디버깅 가능
    #마지막엔 conn.close()로 연결 종료

if __name__ == "__main__":
    main()

#이 파일을 직업 실행했을 때만 main() 실행