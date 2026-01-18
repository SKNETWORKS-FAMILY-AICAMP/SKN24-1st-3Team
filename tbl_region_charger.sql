-- 지역 테이블 명: tbl_region
-- 지역 상세 : tbl_region_detail
-- 전기차 등록수 : tbl_register
-- 충전소 : tbl_station
-- 충전기: tbl_charger 

use evdb;

-- 테이블 삭제
DROP TABLE IF EXISTS tbl_region CASCADE;
DROP TABLE IF EXISTS tbl_charger CASCADE;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS tbl_region
(
    zcode    CHAR(2) NOT NULL COMMENT '지역CODE',
    regionNm    VARCHAR(6) NOT NULL COMMENT '지역명',   -- 서울, 부산...
    CONSTRAINT pk_tbl_region PRIMARY KEY (zcode)
) ENGINE=INNODB COMMENT '지역';


CREATE TABLE IF NOT EXISTS tbl_charger
(
    statid    CHAR(8) NOT NULL COMMENT '충전소ID',
    statNm    VARCHAR(150) NOT NULL COMMENT '충전소이름',
    addr    VARCHAR(180) NOT NULL COMMENT '주소',
    lat DECIMAL(11,8) NOT NULL COMMENT '위도',
    lng DECIMAL(11,8) NOT NULL COMMENT '경도',
    parkingFree VARCHAR(1) COMMENT '주차무료여부',  -- 값 없는 경우도 존재
    limitYn VARCHAR(1) COMMENT '이용자제한',
    limitDetail VARCHAR(150) COMMENT '이용제한사유',  -- 줄글이라서
    zscode CHAR(5) NOT NULL COMMENT '지역상세CODE',
    CONSTRAINT pk_tbl_charger PRIMARY KEY (statid),
    CONSTRAINT fk_zscode FOREIGN KEY (zscode) REFERENCES tbl_region_detail (zscode)
) ENGINE=INNODB COMMENT '충전소';








	