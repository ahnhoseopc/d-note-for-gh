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
drop table OCMOPR06 ;

/* 수숧기록지 */
create table OCMOPR06 (
    OCM06STATUS	    VARCHAR2 (3 Byte)	    , /* STATUS(OPG : GY수술기록지, OP2:일반수술기록지) */
    OCM06IDNOA	    CHAR (7 Byte)	NOT NULL, /* 환자번호 */
    OCM06IDNOB	    CHAR (1 Byte)	NOT NULL, /* 타급종구분 */
    OCM06LWDAT	    CHAR (8 Byte)	NOT NULL, /* 래원 및 입원일 */
    OCM06OPDAT	    CHAR (8 Byte)	NOT NULL, /* 수술일 */
    OCM06SEQNO	    NUMBER (2)	    NOT NULL, /* SEQNO */
    OCM06IOCD	    CHAR (1 Byte)	        , /* I/O 구분 */
    OCM06DV	        CHAR (1 Byte)	        , /* 구분 */
    OCM06CMTA	    VARCHAR2 (2000 Byte)	, /* 마취방법의 기타 */
    OCM06CMTB	    VARCHAR2 (4000 Byte)	, /* 수술기록1 */
    OCM06CMTC	    VARCHAR2 (4000 Byte)	, /* 수술기록2 */
    OCM06MEMO	    VARCHAR2 (200 Byte)	    , /* 메모 */

    OCM06RGCD	    NUMBER (6)	            , /* 등록의 */
    OCM06SYSTM	    CHAR (8 Byte)	        , /* 등록시간 */
    OCM06SYSDAT	    CHAR (8 Byte)	        , /* 등록일자 */

    OCM06IMGFILE10	VARCHAR2 (100 Byte)	    , /* 이미지파일명 */
    OCM06IMGCORD11	VARCHAR2 (4000 Byte)	, /* 이미지코드 */
    OCM06IMGCORD12	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD13	VARCHAR2 (4000 Byte)	,
    OCM06IMGFILE20	VARCHAR2 (100 Byte)	    , /* 이미지파일명2 */
    OCM06IMGCORD21	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD22	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD23	VARCHAR2 (4000 Byte)	,
    OCM06IMGFILE30	VARCHAR2 (100 Byte)	    , /* 이미지파일명3 */
    OCM06IMGCORD31	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD32	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD33	VARCHAR2 (4000 Byte)	,
    OCM06IMGFILE40	VARCHAR2 (100 Byte)	    , /* 이미지파일명4 */
    OCM06IMGCORD41	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD42	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD43	VARCHAR2 (4000 Byte)	,
    OCM06IMGFILE50	VARCHAR2 (100 Byte)	    , /* 이미지파일명5 */
    OCM06IMGCORD51	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD52	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD53	VARCHAR2 (4000 Byte)	,
    OCM06IMGFILE60	VARCHAR2 (100 Byte)	    , /* 이미지파일명6 */
    OCM06IMGCORD61	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD62	VARCHAR2 (4000 Byte)	,
    OCM06IMGCORD63	VARCHAR2 (4000 Byte)	,
    OCM06OBSTOPNN	VARCHAR2 (4000 Byte)	, /* OBSTOPNN4000 */
    OCM06HMRRDGRE	VARCHAR2 (1 Byte)	,
    OCM06REOPYN	    VARCHAR2 (1 Byte)	,
    OCM06KWA	    VARCHAR2 (10 Byte)	,
    OCM06SPTH	    VARCHAR2 (6 Byte)	, /* 주치의(진료과장) */
    OCM06TISSUEEXMN	VARCHAR2 (1 Byte)	,
    OCM06DRNGPIPE	VARCHAR2 (1 Byte)	,
    OCM06ALARM	    VARCHAR2 (2 Byte)	,
    CMPLYN	        VARCHAR2 (1 Byte)	,
    OCM06EMDV	    VARCHAR2 (2 Byte)	,
    OCM06DRNGPIPECNTS	VARCHAR2 (50 Byte)	,
    OCM06TISSUEEXMNCNTS	VARCHAR2 (50 Byte)	,
    OCM06PCLR	    VARCHAR2 (4000 Byte)	,
    OCM06MDTRPLAN	VARCHAR2 (4000 Byte)	,
    OCM06OPPRGR	    CLOB	,
    OCM06OPENDTM	DATE	,
    OCM06OPSTARTTM	DATE	,
    RGSTDT	        DATE	,
    OCM06RGSTNO	    NUMBER	,
    CONSTRAINT constraint_name PRIMARY KEY (OCM06IDNOA, OCM06IDNOB, OCM06LWDAT, OCM06OPDAT, OCM06SEQNO)
);

INSERT INTO OCMOPR06 (
    OCM06STATUS	,                                  /* 수술지구분 */
    OCM06IDNOA	, OCM06IDNOB	,                  /* 환자번호, 타급종구분 */
    OCM06LWDAT	, OCM06OPDAT	, OCM06SEQNO	,  /* 내원 및 입원일, 수술일, 순서 */
    OCM06IOCD   , OCM06DV	    ,                  /* IO구분, 구분, */
    OCM06CMTA	, OCM06CMTB	    , OCM06CMTC   	,  /* 마취방법, 수술기록1, 수술기록2 */
    OCM06RGCD   , OCM06SYSTM    , OCM06SYSDAT	,  /* 등록의, 등록시간, 등록일 */
    OCM06IMGFILE10                                 /* 이미지파일명 */
) VALUES ('OPG', '1028541', '1', '20241106', '20241107', 1, 
          'I', 'A', '마취방법', '수술기록1', '수술기록2', 
          000123, '11:23:45', '20241105', '이미지파일');
INSERT INTO OCMOPR06 (
    OCM06STATUS	,                                  /* 수술지구분 */
    OCM06IDNOA	, OCM06IDNOB	,                  /* 환자번호, 타급종구분 */
    OCM06LWDAT	, OCM06OPDAT	, OCM06SEQNO	,  /* 내원 및 입원일, 수술일, 순서 */
    OCM06IOCD   , OCM06DV	    ,                  /* IO구분, 구분, */
    OCM06CMTA	, OCM06CMTB	    , OCM06CMTC   	,  /* 마취방법, 수술기록1, 수술기록2 */
    OCM06RGCD   , OCM06SYSTM    , OCM06SYSDAT	,  /* 등록의, 등록시간, 등록일 */
    OCM06IMGFILE10                                 /* 이미지파일명 */
) VALUES ('OPG', '1028542', '1', '20241106', '20241107', 1, 
          'I', 'A', '마취방법', '수술기록1', '수술기록2', 
          000123, '11:23:45', '20241105', '이미지파일');
INSERT INTO OCMOPR06 (
    OCM06STATUS	,                                  /* 수술지구분 */
    OCM06IDNOA	, OCM06IDNOB	,                  /* 환자번호, 타급종구분 */
    OCM06LWDAT	, OCM06OPDAT	, OCM06SEQNO	,  /* 내원 및 입원일, 수술일, 순서 */
    OCM06IOCD   , OCM06DV	    ,                  /* IO구분, 구분, */
    OCM06CMTA	, OCM06CMTB	    , OCM06CMTC   	,  /* 마취방법, 수술기록1, 수술기록2 */
    OCM06RGCD   , OCM06SYSTM    , OCM06SYSDAT	,  /* 등록의, 등록시간, 등록일 */
    OCM06IMGFILE10                                 /* 이미지파일명 */
) VALUES ('OPG', '1028543', '1', '20241106', '20241107', 1, 
          'I', 'A', '마취방법', '수술기록1', '수술기록2', 
          000123, '11:23:45', '20241105', '이미지파일');
INSERT INTO OCMOPR06 (
    OCM06STATUS	,                                  /* 수술지구분 */
    OCM06IDNOA	, OCM06IDNOB	,                  /* 환자번호, 타급종구분 */
    OCM06LWDAT	, OCM06OPDAT	, OCM06SEQNO	,  /* 내원 및 입원일, 수술일, 순서 */
    OCM06IOCD   , OCM06DV	    ,                  /* IO구분, 구분, */
    OCM06CMTA	, OCM06CMTB	    , OCM06CMTC   	,  /* 마취방법, 수술기록1, 수술기록2 */
    OCM06RGCD   , OCM06SYSTM    , OCM06SYSDAT	,  /* 등록의, 등록시간, 등록일 */
    OCM06IMGFILE10                                 /* 이미지파일명 */
) VALUES ('OPG', '1028544', '1', '20241106', '20241107', 1, 
          'I', 'A', '마취방법', '수술기록1', '수술기록2', 
          000123, '11:23:45', '20241105', '이미지파일');
INSERT INTO OCMOPR06 (
    OCM06STATUS	,                                  /* 수술지구분 */
    OCM06IDNOA	, OCM06IDNOB	,                  /* 환자번호, 타급종구분 */
    OCM06LWDAT	, OCM06OPDAT	, OCM06SEQNO	,  /* 내원 및 입원일, 수술일, 순서 */
    OCM06IOCD   , OCM06DV	    ,                  /* IO구분, 구분, */
    OCM06CMTA	, OCM06CMTB	    , OCM06CMTC   	,  /* 마취방법, 수술기록1, 수술기록2 */
    OCM06RGCD   , OCM06SYSTM    , OCM06SYSDAT	,  /* 등록의, 등록시간, 등록일 */
    OCM06IMGFILE10                                 /* 이미지파일명 */
) VALUES ('OPG', '1028545', '1', '20241106', '20241107', 1, 
          'I', 'A', '마취방법', '수술기록1', '수술기록2', 
          000123, '11:23:45', '20241105', '이미지파일');

COMMIT;

select OCM06STATUS	,                                  /* 수술지구분 */
    OCM06IDNOA	, OCM06IDNOB	,                  /* 환자번호, 타급종구분 */
    OCM06LWDAT	, OCM06OPDAT	, OCM06SEQNO	,  /* 내원 및 입원일, 수술일, 순서 */
    OCM06IOCD   , OCM06DV	    ,                  /* IO구분, 구분, */
    OCM06CMTA	, OCM06CMTB	    , OCM06CMTC   	,  /* 마취방법, 수술기록1, 수술기록2 */
    OCM06RGCD   , OCM06SYSTM    , OCM06SYSDAT	,  /* 등록의, 등록시간, 등록일 */
    OCM06IMGFILE10                                 /* 이미지파일명 */
from OCMOPR06;
select * from all_tables;


