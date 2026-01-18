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

LOAD DATA LOCAL INFILE 'C:/PMO/02_mysql/1st_project_sql/ev_chargers_data.csv' INTO TABLE tbl_charger
FIELDS TERMINATED BY ','
ENCLOSED BY '"'				-- ""로 묶인 부분에 대해서는 ,를 구분자로 간주하지 않게 하기 위해
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @dummy,        -- statNm (필요없음)
    @vstatId,      -- statId
    @vchgerId,     -- chgerId
    @vchgerType,   -- chgerType
    @dummy,        -- addr (필요없음)
    @dummy,        -- addrDetail (필요없음)
    @dummy,        -- location (필요없음)
    @vuseTime,     -- useTime
    @dummy,        -- lat (필요없음)
    @dummy,        -- lng (필요없음)
    @dummy,        -- busiId (필요없음)
    @dummy,        -- bnm (필요없음)
    @dummy,        -- busiNm (필요없음)
    @dummy,        -- busiCall (필요없음)
    @vstat,        -- stat
    @dummy,        -- statUpdDt (필요없음)
    @dummy,        -- lastTsdt (필요없음)
    @dummy,        -- lastTedt (필요없음)
    @dummy,        -- nowTsdt (필요없음)
    @dummy,        -- powerType (필요없음)
    @voutput,      -- output
    @vmethod,      -- method
    @dummy,        -- zcode (필요없음)
    @dummy,        -- zscode (필요없음)
    @dummy,        -- kind (필요없음)
    @dummy,        -- kindDetail (필요없음)
    @dummy,        -- parkingFree (필요없음)
    @dummy,        -- note (필요없음)
    @dummy,        -- limitYn (필요없음)
    @dummy,        -- limitDetail (필요없음)
    @dummy,        -- delYn (필요없음)
    @dummy,        -- delDetail (필요없음)
    @dummy,        -- trafficYn (필요없음)
    @vyear,        -- year (필요없음)
    @vfloorNum,    -- floorNum
    @vfloorType,   -- floorType
    @dummy         -- maker (필요없음)
)
SET 
    statId = @vstatId,
    chgerId = @vchgerId,
    chgerType = @vchgerType,
	useTime = @vuseTime,
    stat = @vstat,
    output = @voutput,
    method = @vmethod,
    install_year = @vyear,
    floorNum = @vfloorNum,
    floorType = @vfloorType;