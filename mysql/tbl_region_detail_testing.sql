use evdb;

DROP TABLE IF Exists tbl_region_detail;

CREATE TABLE IF NOT EXISTS tbl_region_detail
(
	zscode CHAR(5) NOT NULL COMMENT '지역상세CODE',
    regionDetailNm VARCHAR(30) NOT NULL COMMENT '지역상세명', 	-- 제일 긴 이름은 세종특별자치시이고 그보다 더 여유를 두었습니다
    zcode CHAR(2) NOT NULL COMMENT '지역CODE',
    
    PRIMARY KEY (zscode)    
) ENGINE=InnoDB;

LOAD DATA LOCAL INFILE 'C:/PMO/02_mysql/ev_region_detail.csv' INTO TABLE tbl_region_detailtbl_region_detail
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @vzscode,           -- csv를 보면 코드 뒤에 공백이 있습니다.
    @vregionDetailNm,	-- 이 또한 이름 뒤에 공백이 있습니다.
    @vzcode				-- 유일하게 공백이 없는 항목
)
SET 
    zscode = TRIM(@vzscode),            		-- 양옆의 공백을 제거한 뒤 테이블에 넣습니다
    regionDetailNm = TRIM(@vregionDetailNm),	-- 위와 같은 행위
    zcode = @vzcode;