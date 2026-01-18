USE evdb;

-- tbl_register라는 테이블 생성

#create table: 테이블 생성
CREATE TABLE tbl_register (
  year INT NOT NULL,
  region VARCHAR(30) NOT NULL,
  registrations INT NOT NULL,
  PRIMARY KEY (year, region)
); #primary key를 중복으로 지정

#tbl_register에 year, region, registerations라는 행 생성
INSERT INTO tbl_register (year, region, registrations)

#tbl_register에서 year, seoul을 가져옴
SELECT year, '서울', seoul FROM tbl_register
UNION ALL SELECT year, '부산', busan FROM tbl_register
UNION ALL SELECT year, '대구', daegu FROM tbl_register
UNION ALL SELECT year, '인천', incheon FROM tbl_register
UNION ALL SELECT year, '광주', gwangju FROM tbl_register
UNION ALL SELECT year, '대전', daejeon FROM tbl_register
UNION ALL SELECT year, '울산', ulsan FROM tbl_register
UNION ALL SELECT year, '세종', sejong FROM tbl_register
UNION ALL SELECT year, '경기', gyeonggi FROM tbl_register
UNION ALL SELECT year, '강원', gangwon FROM tbl_register
UNION ALL SELECT year, '충북', chungbuk FROM tbl_register
UNION ALL SELECT year, '충남', chungnam FROM tbl_register
UNION ALL SELECT year, '전북', jeonbuk FROM tbl_register
UNION ALL SELECT year, '전남', jeonnam FROM tbl_register
UNION ALL SELECT year, '경북', gyeongbuk FROM tbl_register
UNION ALL SELECT year, '경남', gyeongnam FROM tbl_register
UNION ALL SELECT year, '제주', jeju FROM tbl_register;

#전체를 조회하는 코드 -> 원래는 열을 하나하나 다 써야 하지만 편의상...!
SELECT *
FROM tbl_register
ORDER BY year DESC, region;
