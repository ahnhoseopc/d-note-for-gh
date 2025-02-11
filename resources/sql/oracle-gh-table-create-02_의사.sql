--
-- RUN AS SYSTEM
--
-- CREATE USER hoseop IDENTIFIED BY "mypasswd!@" DEFAULT TABLESPACE users;
-- GRANT CREATE SESSION TO hoseop;
-- GRANT CREATE TABLE TO hoseop;
-- ALTER USER hoseop QUOTA UNLIMITED ON users;
ALTER USER hoseop DEFAULT tablespace USERS;

--
-- RUN AS HOSEOP
--
drop table JAIN_OCS.OCMDCT02 ;

/* 수숧기록지 */
create table JAIN_OCS.OCMDCT02 (
    OCM02RGCD   CHAR (6 Byte)	    ,	/* 담당의(레지던트,진료과장) */
    OCM02RGNM   VARCHAR (40 Byte)   ,   /* 담당의이름 */

    OCM02HPDAT	CHAR (8 Byte)       ,	/* 입사일 */
    OCM02RTDAT	CHAR (8 Byte)       ,	/* 퇴원일 */

    OCM02SYSDAT VARCHAR2 (8 Byte)	,	/* 등록날짜 */
    OCM02SYSTM  VARCHAR2 (8 Byte)	,	/* 등록시간 */

    CONSTRAINT OCMDCT02_PK PRIMARY KEY (OCM02RGCD) /* 담당의 */
);

INSERT INTO JAIN_OCS.OCMDCT02 (
    OCM02RGCD	, OCM02RGNM     ,                  /* 수술지구분 */
    OCM02HPDAT	, OCM02RTDAT	,                  /* 환자번호, 타급종구분 */
    OCM02SYSDAT	, OCM02SYSTM                       /* 내원 및 입원일, 수술일, 순서 */
) VALUES ('000123', '박의사', '20200106', '', '20200106', '11:23:45');

INSERT INTO JAIN_OCS.OCMDCT02 (
    OCM02RGCD	, OCM02RGNM     ,                  /* 수술지구분 */
    OCM02HPDAT	, OCM02RTDAT	,                  /* 환자번호, 타급종구분 */
    OCM02SYSDAT	, OCM02SYSTM                       /* 내원 및 입원일, 수술일, 순서 */
) VALUES ('000023', '최의사', '20150106', '20231106', '20200106', '11:23:45');

INSERT INTO JAIN_OCS.OCMDCT02 (
    OCM02RGCD	, OCM02RGNM     ,                  /* 수술지구분 */
    OCM02HPDAT	, OCM02RTDAT	,                  /* 환자번호, 타급종구분 */
    OCM02SYSDAT	, OCM02SYSTM                       /* 내원 및 입원일, 수술일, 순서 */
) VALUES ('100123', '안의사', '20180106', '', '20200106', '11:23:45');

INSERT INTO JAIN_OCS.OCMDCT02 (
    OCM02RGCD	, OCM02RGNM     ,                  /* 수술지구분 */
    OCM02HPDAT	, OCM02RTDAT	,                  /* 환자번호, 타급종구분 */
    OCM02SYSDAT	, OCM02SYSTM                       /* 내원 및 입원일, 수술일, 순서 */
) VALUES ('200123', '오의사', '20210106', '', '20200106', '11:23:45');

INSERT INTO JAIN_OCS.OCMDCT02 (
    OCM02RGCD	, OCM02RGNM     ,                  /* 수술지구분 */
    OCM02HPDAT	, OCM02RTDAT	,                  /* 환자번호, 타급종구분 */
    OCM02SYSDAT	, OCM02SYSTM                       /* 내원 및 입원일, 수술일, 순서 */
) VALUES ('210123', '하의사', '20220106', '20241106', '20200106', '11:23:45');

COMMIT;

select                                   /* 수술지구분 */
    OCM02RGCD	, OCM02RGNM     ,                  /* 수술지구분 */
    OCM02HPDAT	, OCM02RTDAT	,                  /* 환자번호, 타급종구분 */
    OCM02SYSDAT	, OCM02SYSTM                       /* 내원 및 입원일, 수술일, 순서 */
from JAIN_OCS.OCMDCT02;




