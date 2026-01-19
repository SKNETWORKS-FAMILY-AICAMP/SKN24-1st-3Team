-- 지역 테이블 명: tbl_region
-- 지역 상세 : tbl_region_detail
-- 전기차 등록수 : tbl_register
-- 충전소 : tbl_station
-- 충전기: tbl_charger 

use evdb;

-- 테이블 삭제
DROP TABLE IF EXISTS tbl_region;
DROP TABLE IF EXISTS tbl_region_detail;
DROP TABLE IF EXISTS tbl_register;
DROP TABLE IF EXISTS tbl_station;
DROP TABLE IF EXISTS tbl_charger;


-- 지역 테이블 생성 tbl_region
CREATE TABLE IF NOT EXISTS tbl_region
(
    zcode    CHAR(2) NOT NULL COMMENT '지역CODE',
    regionNm    VARCHAR(6) NOT NULL COMMENT '지역명',   -- 서울, 부산...
    CONSTRAINT pk_tbl_region PRIMARY KEY (zcode)
) ENGINE=INNODB COMMENT '지역';



-- 전기차 등록수 테이블 생성 tbl_register
CREATE TABLE tbl_register (
  year INT NOT NULL COMMENT '연도',
  zcode    CHAR(2) NOT NULL COMMENT '지역CODE',
  registrations INT NOT NULL COMMENT '등록대수',
  CONSTRAINT pk_tbl_register PRIMARY KEY (year, zcode),
  CONSTRAINT fk_zcode FOREIGN KEY (zcode) REFERENCES tbl_region (zcode)
) ENGINE=INNODB COMMENT '전기차 등록수';




-- 지역상세 테이블 생성
CREATE TABLE IF NOT EXISTS tbl_region_detail (
    zscode CHAR(5) NOT NULL COMMENT '지역상세CODE',
    regionDetailNm VARCHAR(30) NOT NULL COMMENT '지역상세명',
    zcode CHAR(2) NOT NULL COMMENT '지역CODE',
    
    CONSTRAINT pk_tbl_region_detail PRIMARY KEY (zscode),
    CONSTRAINT fk_region_detail_zcode_ref FOREIGN KEY (zcode)
        REFERENCES tbl_region(zcode)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=INNODB COMMENT='지역상세';


-- -- 1. 현재 세션에서 LOCAL 허용 상태 확인
-- SHOW VARIABLES LIKE 'local_infile';

-- -- 2. 만약 OFF이면 세션/글로벌에서 켬
-- SET GLOBAL local_infile = 1;
-- SET SESSION local_infile = 1;



-- -- 현재 세션 활성화
-- -- 그냥 ev_region_detail.csv를 쓰면 오류났었고, 절대 경로 쓰는 게 확실하더라고요.
-- LOAD DATA LOCAL INFILE 'C:/SKN24/SKN24-1st-3Team/ev_region_detail.csv' INTO TABLE tbl_region_detail
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (
--     @vzscode,           -- csv를 보면 코드 뒤에 공백이 있습니다.
--     @vregionDetailNm,	-- 이 또한 이름 뒤에 공백이 있습니다.
--     @vzcode				-- 유일하게 공백이 없는 항목
-- )
-- SET 
--     zscode = TRIM(@vzscode),            		-- 양옆의 공백을 제거한 뒤 테이블에 넣습니다
--     regionDetailNm = TRIM(@vregionDetailNm),	-- 위와 같은 행위
--     zcode = @vzcode;




-- 충전소 테이블 생성 tbl_station
CREATE TABLE IF NOT EXISTS tbl_station
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
    CONSTRAINT pk_tbl_station PRIMARY KEY (statid),
    CONSTRAINT fk_zscode FOREIGN KEY (zscode) REFERENCES tbl_region_detail (zscode)
) ENGINE=INNODB COMMENT '충전소';



-- 충전기 테이블 생성 tbl_charger

use evdb;

DROP TABLE IF Exists tbl_charger;

CREATE TABLE IF NOT EXISTS tbl_charger
(
    statId	CHAR(8) NOT NULL COMMENT '충전소ID',
    chgerId	CHAR(2) NOT NULL COMMENT '충전기ID', 			-- chgerId는 0으로 시작하는 숫자 2자리 형태라 CHAR로 하는 게 맞아보입니다
    chgerType CHAR(2) NOT NULL COMMENT '충전기타입', 		-- 위와 동일한 사유로 CHAR 2로 하겠습니다
    stat DECIMAL(1,0) NOT NULL COMMENT '충전기상태', 		-- 한자리 숫자 값을 가집니다
    output DECIMAL(3,0) NOT NULL COMMENT '충전기용량', 	-- 3, 7, 50, 100, 200 중 하나의 값을 가집니다
    method CHAR(6) NOT NULL COMMENT '충전기방식', 			-- 갖는 값이 단독/동시 중 하나이므로 CHAR 6
    install_year DECIMAL(4,0) NOT NULL COMMENT '설치년도', -- CSV의 year 데이터를 여기에 넣습니다
    floorNum INT NOT NULL COMMENT '지상/지하 층수',
    floorType CHAR(1) NOT NULL COMMENT '지상/지하 구분', 	-- F/B 중 하나의 값을 가지므로 CHAR(1)
    useTime VARCHAR(100) NOT NULL COMMENT '이용가능시간', 	-- 줄글이라서 넉넉히 하였다
    
    PRIMARY KEY (statId, chgerId), 						-- 충전소ID, 충전기ID를 복합키로 하여 식별하도록 한다
 
	CONSTRAINT station_to_charger 						-- 외래 키를 설정하기 위한 규칙 이름 달기
		FOREIGN KEY (statId) REFERENCES tbl_station(statId) -- 우리 테이블의 statId는 tbl_station의 statID에 실제로 존재하는 값이어야 한다는 의미
        ON DELETE CASCADE ON UPDATE CASCADE 				-- tbl_station에서 충전소 하나가 삭제되면 해당 충전소의 충전기도 모두 삭제되도록
    
) ENGINE=InnoDB;

-- ALTER TABLE tbl_charger
-- MODIFY floorNum INT NULL COMMENT '지상/지하 층수',
-- MODIFY floorType CHAR(1) NULL COMMENT '지상/지하 구분';


-- LOAD DATA LOCAL INFILE 'C:/SKN24/EV_CRAWLING/ev_chargers_data (2).csv' INTO TABLE tbl_charger
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'				-- ""로 묶인 부분에 대해서는 ,를 구분자로 간주하지 않게 하기 위해
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (
--     @dummy,        -- statNm (필요없음)
--     @vstatId,      -- statId
--     @vchgerId,     -- chgerId
--     @vchgerType,   -- chgerType
--     @dummy,        -- addr (필요없음)
--     @dummy,        -- addrDetail (필요없음)
--     @dummy,        -- location (필요없음)
--     @vuseTime,     -- useTime
--     @dummy,        -- lat (필요없음)
--     @dummy,        -- lng (필요없음)
--     @dummy,        -- busiId (필요없음)
--     @dummy,        -- bnm (필요없음)
--     @dummy,        -- busiNm (필요없음)
--     @dummy,        -- busiCall (필요없음)
--     @vstat,        -- stat
--     @dummy,        -- statUpdDt (필요없음)
--     @dummy,        -- lastTsdt (필요없음)
--     @dummy,        -- lastTedt (필요없음)
--     @dummy,        -- nowTsdt (필요없음)
--     @dummy,        -- powerType (필요없음)
--     @voutput,      -- output
--     @vmethod,      -- method
--     @dummy,        -- zcode (필요없음)
--     @dummy,        -- zscode (필요없음)
--     @dummy,        -- kind (필요없음)
--     @dummy,        -- kindDetail (필요없음)
--     @dummy,        -- parkingFree (필요없음)
--     @dummy,        -- note (필요없음)
--     @dummy,        -- limitYn (필요없음)
--     @dummy,        -- limitDetail (필요없음)
--     @dummy,        -- delYn (필요없음)
--     @dummy,        -- delDetail (필요없음)
--     @dummy,        -- trafficYn (필요없음)
--     @vyear,        -- year (필요없음)
--     @vfloorNum,    -- floorNum
--     @vfloorType,   -- floorType
--     @dummy         -- maker (필요없음)
-- )
-- SET 
--     statId = @vstatId,
--     chgerId = @vchgerId,
--     chgerType = @vchgerType,
-- 	useTime = @vuseTime,
--     stat = @vstat,
--     output = @voutput,
--     method = @vmethod,
--     install_year = @vyear,
--     floorNum = @vfloorNum,
--     floorType = @vfloorType;





	