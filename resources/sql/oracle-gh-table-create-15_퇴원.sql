--
-- RUN AS SYSTEM
--
-- CREATE USER hoseop IDENTIFIED BY "mypasswd!@" DEFAULT TABLESPACE users;
-- GRANT CREATE SESSION TO hoseop;
-- GRANT CREATE TABLE TO hoseop;
-- ALTER USER hoseop QUOTA UNLIMITED ON users;
-- ALTER USER hoseop DEFAULT tablespace USERS;

--
-- RUN AS HOSEOP
--
drop table JAIN_OCS.OCMRTN32 ;

/* 퇴원원기록지 */
create table JAIN_OCS.OCMRTN32 (
    OCM32STATUS	CHAR (2 Byte)       	,	/* STATUS */
    OCM32IDNOA	CHAR (8 Byte)	NOT NULL,	/* 환자번호 */
    OCM32IDNOB	CHAR (8 Byte)	NOT NULL,	/* 타급종구분 */
    OCM32LWDAT	CHAR (8 Byte)	NOT NULL,	/* 래원 및 입원 */
    OCM32IOCD	CHAR (1 Byte)       	,	/* I/O구분 */
    OCM32BHCD	CHAR (2 Byte)       	,	/* 급종 */
    OCM32HPDAT	CHAR (8 Byte)       	,	/* 입원일 */
    OCM32RTDAT	CHAR (8 Byte)       	,	/* 퇴원일 */
    OCM32KWA	CHAR (2 Byte)       	,	/* 성별 */
    OCM32WARD   	VARCHAR2 (6 Byte)	,	/* BEDNO */
    OCM32CHIEFCOMP	VARCHAR2 (3000 Byte),	/* CHIEF COMPLAINTS */
    OCM32FINALDX	VARCHAR2 (3000 Byte),	/* FINAL DX */
    OCM32OP     	VARCHAR2 (3000 Byte),	/* TREATMENT OP */
    OCM32MEDICAL	VARCHAR2 (3000 Byte),   /* TREATMENT MEDICAL */
    OCM32FOLLOW 	VARCHAR2 (3000 Byte),	/* FOLLOW-UP PLAN */
    OCM32OTHER  	VARCHAR2 (3000 Byte),	/* OTHER REMARKS */

    OCM32SPTH   	CHAR (6 Byte)   	,	/* 주치의(진료과장) */
    
    OCM32SEX    	CHAR (1 Byte)	    ,	/* 성별 */
    OCM32AGE    	VARCHAR2 (7 Byte)	,	/* 나이 */
    OCM32RTRSTCD	CHAR (2 Byte)	    ,	/* 치료결과코드 */
    OCM32RTTYPECD	CHAR (2 Byte)   	,	/* 퇴원형태코드 */
    OCM32RTHSPNM	VARCHAR2 (100 Byte)	,	/* 전원병원명 */
    OCM32RTCMT  	VARCHAR2 (100 Byte)	,	/* 기타CMT */
    OCM32SCNDDX 	VARCHAR2 (3000 Byte),	/* 부진단명 */
    OCM32PI     	VARCHAR2 (600 Byte)	,	
    OCM32PHX    	VARCHAR2 (600 Byte)	,	
    OCM32DM     	VARCHAR2 (1 Byte)	,	
    OCM32TBC    	VARCHAR2 (1 Byte)	,	
    OCM32HT     	VARCHAR2 (1 Byte)	,	
    OCM32AST    	VARCHAR2 (1 Byte)	,	

    OCM32RGCD   	VARCHAR2 (6 Byte)	,	/* 담당의(레지던트,진료과장) */
    OCM32SYSDAT 	VARCHAR2 (8 Byte)	,	/* 등록날짜 */
    OCM32SYSTM  	VARCHAR2 (8 Byte)	,	/* 등록시간 */

    OCM32RTRSTTXT	VARCHAR2 (50 Byte)	,	
    OCM32PROBLEM	CLOB	            ,  /* 중요검사소견 */
    CONSTRAINT OCMRTN32_PK PRIMARY KEY (OCM32IDNOA, OCM32IDNOB, OCM32LWDAT) /*환자번호, 타급종구분, 래원 및 입원 */
);

INSERT INTO JAIN_OCS.OCMRTN32 (
OCM32STATUS	,	/* STATUS */
OCM32IDNOA	, OCM32IDNOB	, OCM32LWDAT	,  /* 환자번호, 타급종구분, 래원 및 입원 */
OCM32IOCD	, OCM32BHCD	    ,                  /* I/O구분, 급종 */
OCM32HPDAT	, OCM32RTDAT	,                  /* 입원일, 퇴원일 */
OCM32KWA	, OCM32WARD	    ,                  /* 성별, BEDNO */
OCM32CHIEFCOMP, OCM32FINALDX, OCM32OP       ,  /* CHIEF COMPLAINTS, FINAL DX, TREATMENT OP */
OCM32MEDICAL, OCM32FOLLOW	, OCM32OTHER    ,  /* TREATMENT MEDICAL, FOLLOW-UP PLAN, OTHER REMARKS */
OCM32SPTH	, OCM32SEX	    , OCM32AGE	    ,  /* 주치의(진료과장), 성별, 나이 */
OCM32RTRSTCD, OCM32RTTYPECD	, OCM32RTHSPNM	,  /* 치료결과코드, 퇴원형태코드, 전원병원명 */
OCM32RTCMT	, OCM32SCNDDX	,                  /* 기타CMT, 부진단명 */
OCM32PI     , OCM32PHX      , OCM32DM       ,
OCM32TBC    , OCM32HT       , OCM32AST	    ,	
OCM32SYSDAT	, OCM32SYSTM	,                  /* 등록날짜. 등록시간, 담당의(레지턴트,가정) */
OCM32RGCD	, OCM32RTRSTTXT , OCM32PROBLEM     /* 담당의(레지던트,진료과장), 중요검사소견 */
) VALUES ('RT', '1028542', '1', '20241106',
          'I', 'AB', '20241106', '20241110', '02', '0908', 
          '주호소', '주진단명', '수술명', '처치명', '추후관리계획', '비고',
          '000123', 'M', '53', '20', '10','전원병원','기타CMT','부진단명',
          'PI600','PHX600','D','T','H','A',
          '20241110','12:30:40','000123','RTRSTTXT50','PROBLEM_CLOB');

INSERT INTO JAIN_OCS.OCMRTN32 (
OCM32STATUS	,	/* STATUS */
OCM32IDNOA	, OCM32IDNOB	, OCM32LWDAT	,  /* 환자번호, 타급종구분, 래원 및 입원 */
OCM32IOCD	, OCM32BHCD	    ,                  /* I/O구분, 급종 */
OCM32HPDAT	, OCM32RTDAT	,                  /* 입원일, 퇴원일 */
OCM32KWA	, OCM32WARD	    ,                  /* 성별, BEDNO */
OCM32CHIEFCOMP, OCM32FINALDX, OCM32OP       ,  /* CHIEF COMPLAINTS, FINAL DX, TREATMENT OP */
OCM32MEDICAL, OCM32FOLLOW	, OCM32OTHER    ,  /* TREATMENT MEDICAL, FOLLOW-UP PLAN, OTHER REMARKS */
OCM32SPTH	, OCM32SEX	    , OCM32AGE	    ,  /* 주치의(진료과장), 성별, 나이 */
OCM32RTRSTCD, OCM32RTTYPECD	, OCM32RTHSPNM	,  /* 치료결과코드, 퇴원형태코드, 전원병원명 */
OCM32RTCMT	, OCM32SCNDDX	,                  /* 기타CMT, 부진단명 */
OCM32PI     , OCM32PHX      , OCM32DM       ,
OCM32TBC    , OCM32HT       , OCM32AST	    ,	
OCM32SYSDAT	, OCM32SYSTM	,                  /* 등록날짜. 등록시간, 담당의(레지턴트,가정) */
OCM32RGCD	, OCM32RTRSTTXT , OCM32PROBLEM     /* 담당의(레지던트,진료과장), 중요검사소견 */
) VALUES ('RT', '1028541', '1', '20241106',
          'I', 'AB', '20241106', '20241110', '02', '0908', 
          '주호소', '주진단명', '수술명', '처치명', '추후관리계획', '비고',
          '000123', 'M', '53', '20', '10','전원병원','기타CMT','부진단명',
          'PI600','PHX600','D','T','H','A',
          '20241110','12:30:40','000123','RTRSTTXT50','PROBLEM_CLOB');

INSERT INTO JAIN_OCS.OCMRTN32 (
OCM32STATUS	,	/* STATUS */
OCM32IDNOA	, OCM32IDNOB	, OCM32LWDAT	,  /* 환자번호, 타급종구분, 래원 및 입원 */
OCM32IOCD	, OCM32BHCD	    ,                  /* I/O구분, 급종 */
OCM32HPDAT	, OCM32RTDAT	,                  /* 입원일, 퇴원일 */
OCM32KWA	, OCM32WARD	    ,                  /* 성별, BEDNO */
OCM32CHIEFCOMP, OCM32FINALDX, OCM32OP       ,  /* CHIEF COMPLAINTS, FINAL DX, TREATMENT OP */
OCM32MEDICAL, OCM32FOLLOW	, OCM32OTHER    ,  /* TREATMENT MEDICAL, FOLLOW-UP PLAN, OTHER REMARKS */
OCM32SPTH	, OCM32SEX	    , OCM32AGE	    ,  /* 주치의(진료과장), 성별, 나이 */
OCM32RTRSTCD, OCM32RTTYPECD	, OCM32RTHSPNM	,  /* 치료결과코드, 퇴원형태코드, 전원병원명 */
OCM32RTCMT	, OCM32SCNDDX	,                  /* 기타CMT, 부진단명 */
OCM32PI     , OCM32PHX      , OCM32DM       ,
OCM32TBC    , OCM32HT       , OCM32AST	    ,	
OCM32SYSDAT	, OCM32SYSTM	,                  /* 등록날짜. 등록시간, 담당의(레지턴트,가정) */
OCM32RGCD	, OCM32RTRSTTXT , OCM32PROBLEM     /* 담당의(레지던트,진료과장), 중요검사소견 */
) VALUES ('RT', '1028543', '1', '20241106',
          'I', 'AB', '20241106', '20241110', '02', '0908', 
          '주호소', '주진단명', '수술명', '처치명', '추후관리계획', '비고',
          '000123', 'M', '53', '20', '10','전원병원','기타CMT','부진단명',
          'PI600','PHX600','D','T','H','A',
          '20241110','12:30:40','000123','RTRSTTXT50','PROBLEM_CLOB');

INSERT INTO JAIN_OCS.OCMRTN32 (
OCM32STATUS	,	/* STATUS */
OCM32IDNOA	, OCM32IDNOB	, OCM32LWDAT	,  /* 환자번호, 타급종구분, 래원 및 입원 */
OCM32IOCD	, OCM32BHCD	    ,                  /* I/O구분, 급종 */
OCM32HPDAT	, OCM32RTDAT	,                  /* 입원일, 퇴원일 */
OCM32KWA	, OCM32WARD	    ,                  /* 성별, BEDNO */
OCM32CHIEFCOMP, OCM32FINALDX, OCM32OP       ,  /* CHIEF COMPLAINTS, FINAL DX, TREATMENT OP */
OCM32MEDICAL, OCM32FOLLOW	, OCM32OTHER    ,  /* TREATMENT MEDICAL, FOLLOW-UP PLAN, OTHER REMARKS */
OCM32SPTH	, OCM32SEX	    , OCM32AGE	    ,  /* 주치의(진료과장), 성별, 나이 */
OCM32RTRSTCD, OCM32RTTYPECD	, OCM32RTHSPNM	,  /* 치료결과코드, 퇴원형태코드, 전원병원명 */
OCM32RTCMT	, OCM32SCNDDX	,                  /* 기타CMT, 부진단명 */
OCM32PI     , OCM32PHX      , OCM32DM       ,
OCM32TBC    , OCM32HT       , OCM32AST	    ,	
OCM32SYSDAT	, OCM32SYSTM	,                  /* 등록날짜. 등록시간, 담당의(레지턴트,가정) */
OCM32RGCD	, OCM32RTRSTTXT , OCM32PROBLEM     /* 담당의(레지던트,진료과장), 중요검사소견 */
) VALUES ('RT', '1028544', '1', '20241106',
          'I', 'AB', '20241106', '20241110', '02', '0908', 
          '주호소', '주진단명', '수술명', '처치명', '추후관리계획', '비고',
          '000123', 'M', '53', '20', '10','전원병원','기타CMT','부진단명',
          'PI600','PHX600','D','T','H','A',
          '20241110','12:30:40','000123','RTRSTTXT50','PROBLEM_CLOB');

INSERT INTO JAIN_OCS.OCMRTN32 (
OCM32STATUS	,	/* STATUS */
OCM32IDNOA	, OCM32IDNOB	, OCM32LWDAT	,  /* 환자번호, 타급종구분, 래원 및 입원 */
OCM32IOCD	, OCM32BHCD	    ,                  /* I/O구분, 급종 */
OCM32HPDAT	, OCM32RTDAT	,                  /* 입원일, 퇴원일 */
OCM32KWA	, OCM32WARD	    ,                  /* 성별, BEDNO */
OCM32CHIEFCOMP, OCM32FINALDX, OCM32OP       ,  /* CHIEF COMPLAINTS, FINAL DX, TREATMENT OP */
OCM32MEDICAL, OCM32FOLLOW	, OCM32OTHER    ,  /* TREATMENT MEDICAL, FOLLOW-UP PLAN, OTHER REMARKS */
OCM32SPTH	, OCM32SEX	    , OCM32AGE	    ,  /* 주치의(진료과장), 성별, 나이 */
OCM32RTRSTCD, OCM32RTTYPECD	, OCM32RTHSPNM	,  /* 치료결과코드, 퇴원형태코드, 전원병원명 */
OCM32RTCMT	, OCM32SCNDDX	,                  /* 기타CMT, 부진단명 */
OCM32PI     , OCM32PHX      , OCM32DM       ,
OCM32TBC    , OCM32HT       , OCM32AST	    ,	
OCM32SYSDAT	, OCM32SYSTM	,                  /* 등록날짜. 등록시간, 담당의(레지턴트,가정) */
OCM32RGCD	, OCM32RTRSTTXT , OCM32PROBLEM     /* 담당의(레지던트,진료과장), 중요검사소견 */
) VALUES ('RT', '1028545', '1', '20241106',
          'I', 'AB', '20241106', '20241110', '02', '0908', 
          '주호소', '주진단명', '수술명', '처치명', '추후관리계획', '비고',
          '000123', 'M', '53', '20', '10','전원병원','기타CMT','부진단명',
          'PI600','PHX600','D','T','H','A',
          '20241110','12:30:40','000123','RTRSTTXT50','PROBLEM_CLOB');

COMMIT;

select OCM32STATUS	,	/* STATUS */
OCM32IDNOA	, OCM32IDNOB	, OCM32LWDAT	,  /* 환자번호, 타급종구분, 래원 및 입원 */
OCM32IOCD	, OCM32BHCD	    ,                  /* I/O구분, 급종 */
OCM32HPDAT	, OCM32RTDAT	,                  /* 입원일, 퇴원일 */
OCM32KWA	, OCM32WARD	    ,                  /* 성별, BEDNO */
OCM32CHIEFCOMP, OCM32FINALDX, OCM32OP       ,  /* CHIEF COMPLAINTS, FINAL DX, TREATMENT OP */
OCM32MEDICAL, OCM32FOLLOW	, OCM32OTHER    ,  /* TREATMENT MEDICAL, FOLLOW-UP PLAN, OTHER REMARKS */
OCM32SPTH	, OCM32SEX	    , OCM32AGE	    ,  /* 주치의(진료과장), 성별, 나이 */
OCM32RTRSTCD, OCM32RTTYPECD	, OCM32RTHSPNM	,  /* 치료결과코드, 퇴원형태코드, 전원병원명 */
OCM32RTCMT	, OCM32SCNDDX	,                  /* 기타CMT, 부진단명 */
OCM32PI     , OCM32PHX      , OCM32DM       ,
OCM32TBC    , OCM32HT       , OCM32AST	    ,	
OCM32SYSDAT	, OCM32SYSTM	,                  /* 등록날짜. 등록시간, 담당의(레지턴트,가정) */
OCM32RGCD	, OCM32RTRSTTXT , OCM32PROBLEM     /* 담당의(레지던트,진료과장), 중요검사소견 */
from JAIN_OCS.OCMRTN32;

-- select * from all_tables;
