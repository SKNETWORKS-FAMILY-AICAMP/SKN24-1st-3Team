USE evdb;

-- (선택) 기존 테이블이 있으면 삭제하고 새로 만들기
DROP TABLE IF EXISTS tbl_region;

-- year/region 형태의 LONG 테이블 생성
CREATE TABLE tbl_region (
  year INT NOT NULL,
  region VARCHAR(30) NOT NULL,
  registrations INT NOT NULL,
  PRIMARY KEY (year, region)
);

-- 원본(tbl_register: wide) -> tbl_region(long)로 변환하여 적재
INSERT INTO tbl_region (year, region, registrations)
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

-- 확인
SELECT *
FROM tbl_region
ORDER BY year DESC, region;


