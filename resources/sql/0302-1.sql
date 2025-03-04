--
--
--
WITH NN as (SELECT LEVEL NNPOS FROM DUAL CONNECT BY LEVEL < 8)               -- * 세부수술명 구분 건수 최대 8건까지 지원
    ,OP07 AS (                                                               -- * 수술예약 테이블
        SELECT DISTINCT 
            LOWER(                                                           -- 소문자로 비교
            REPLACE(REPLACE(                                                 -- 중간의 탭문자와 리턴문자 제거
            TRIM(BOTH CHR(10) FROM TRIM(BOTH ' ' FROM                        -- 앞뒤로 공백문자와 뉴라인문자 제거
            SUBSTR(OEY07CMTA,                                                -- | 로 구분된 7번째 항목인 수술명 추출
                    INSTR(OEY07CMTA, '|', 1, 6)+1,                           -- == 수술명은 뉴라인으로 세부수술명 구분
                    INSTR(OEY07CMTA, '|', 1, 7)-INSTR(OEY07CMTA, '|', 1, 6)-1
                )
            )), CHR(9)), CHR(13))
            )  OP07NAME
        FROM JAIN_OCS.OEYOPR07 OPR07 
        WHERE 1=1 -- AND ROWNUM < 100
        AND OEY07IDNOA = '0606479'                                           -- 환자ID와 내원일로 환자의 수술명 조회
        AND OEY07LWDAT = '20250227'                                          -- 환자내원일
        -- AND OEY07SPTH IN ('002806' , '001639')
    )
    ,OP06 AS (                                                               -- * 수술기록 테이블
        SELECT OCM06IDNOA, OCM06LWDAT,OCM06OPDAT,
            SUBSTR(OCM06CMTA, 1, INSTR(OCM06CMTA, '|', 1, 1)-1 ) SPTH,       -- 수술의사
            LOWER(
            REPLACE(REPLACE(                                                 -- 중간의 탭문자와 리턴문자 제거
            TRIM(BOTH CHR(10) FROM TRIM(BOTH ' ' FROM                        -- 앞뒤로 공백문자와 뉴라인문자 제거
            SUBSTR(OCM06CMTA,                                                -- | 로 구분된 9번째 항목인 수술명 추출
                    INSTR(OCM06CMTA, '|', 1, 8)+1,                           -- == 수술명은 뉴라인으로 세부수술명 구분
                    INSTR(OCM06CMTA, '|', 1, 9)-INSTR(OCM06CMTA, '|', 1, 8)-1
                )
            )), CHR(9)), CHR(13))
            )  OP06NAME
            , OCM06CMTB                                                      -- Procedures and Findings
            , OCM06CMTC 
        FROM JAIN_OCS.OCMOPR06
        WHERE 1=1 -- AND ROWNUM < 100
        AND OCM06STATUS IN ('OP2','OPG')                                     -- 수술기록만 추출(일반/산부인과)
        AND OCM06LWDAT >= TO_CHAR(ADD_MONTHS(SYSDATE, -6), 'YYYYMMDD')       -- 최근 6개월 기록만 대상
        And SUBSTR(OCM06CMTA, 1, INSTR(OCM06CMTA, '|', 1, 1)-1) = '002806'   -- 집도할 의사ID '002806' / '001639'
        ORDER BY OCM06OPDAT DESC                                             -- 데이터를 선정할 때 최근 순서대로 함.
    )
SELECT 
    regexp_substr(OP07NAME, '[^'||CHR(10)||'\&]+', 1, NNPOS) OPNAMESUB,      -- 줄바꿈문자와 &문자로 세부수술명 구분
    OP07NAME, OP06NAME,                                                      -- 수술예약테이블의 수술명과 수술기록테이블의 수술명
    CASE WHEN OCM06CMTC IS NULL THEN TO_CLOB(OCM06CMTB)                      -- 조회된 수술절차및소견 기록
         ELSE TO_CLOB(OCM06CMTB) || TO_CLOB(OCM06CMTC) END PROCFIND
FROM OP07
CROSS JOIN NN
LEFT JOIN OP06 
    ON OP06NAME like '%' || regexp_substr(OP07NAME, '[^'||CHR(10)||'\&]+', 1, NNPOS) || '%'
WHERE regexp_substr(OP07NAME, '[^'||CHR(10)||'\&]+', 1, NNPOS) IS NOT NULL
ORDER BY OP06NAME
;