use evdb;

DROP TABLE IF Exists tbl_region_detail;

CREATE TABLE IF NOT EXISTS tbl_region_detail
(
	zscode CHAR(5) NOT NULL COMMENT '지역상세CODE',
    regionDetailNm VARCHAR(30) NOT NULL COMMENT '지역상세명', 	-- 제일 긴 이름은 세종특별자치시이고 그보다 더 여유를 두었습니다
    zcode CHAR(2) NOT NULL COMMENT '지역CODE',
    
    PRIMARY KEY (zscode),									-- zscode 단독 PK
 
	CONSTRAINT region_to_region_detail						-- 외래 키를 설정하기 위한 규칙 이름을 다는 과정
        FOREIGN KEY (zcode) REFERENCES tbl_region(zcode)	-- 우리 테이블의 zcode는 tbl_region의 zcode에 실제로 존재하는 값이어야 한다는 의미입니다
        ON DELETE CASCADE ON UPDATE CASCADE 				-- tbl_region에서 지역 하나가 삭제되면 해당 지역의 상세지역도 모두 삭제되도록
    
) ENGINE=InnoDB;

-- 그냥 ev_region_detail.csv를 쓰면 오류났었고, 절대 경로 쓰는 게 확실하더라고요.
LOAD DATA LOCAL INFILE 'C:/PMO/02_mysql/1st_project_sql/ev_region_detail.csv' INTO TABLE tbl_region_detail
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