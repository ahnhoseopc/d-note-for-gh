--
-- RUN AS SYSTEM
--
-- CREATE USER hoseop IDENTIFIED BY "mypasswd!@";
-- GRANT CREATE SESSION TO hoseop;
-- GRANT CREATE TABLE TO hoseop;
-- ALTER USER hoseop QUOTA UNLIMITED ON users;

--
-- RUN AS HOSEOP
--
drop table OCMPTN01 ;

/* 수숧기록지 */
create table OCMPTN01 (
    OCM01IDNOA	    CHAR (7 Byte)	NOT NULL, /* 환자번호 */
    OCM01NAMEA	    VARCHAR (40 Byte)	    , /* 환자이름 */

    OCM01SYSTM	    CHAR (8 Byte)	        , /* 등록시간 */
    OCM01SYSDAT	    CHAR (8 Byte)	        , /* 등록일자 */

    CONSTRAINT OCMPTN01_PK PRIMARY KEY (OCM01IDNOA)
);

INSERT INTO OCMPTN01 (
    OCM01IDNOA	, OCM01NAMEA	,                  /* 환자번호, 이름름 */
    OCM01SYSDAT	, OCM01SYSTM	                   /* 날짜, 시간 */
) VALUES ('1028541', '김갑동', '20241106', '10:20:30');

INSERT INTO OCMPTN01 (
    OCM01IDNOA	, OCM01NAMEA	,                  /* 환자번호, 이름름 */
    OCM01SYSDAT	, OCM01SYSTM	                   /* 날짜, 시간 */
) VALUES ('0028541', '나을수', '20020806', '10:20:30');

COMMIT;

select 
    OCM01IDNOA	, OCM01NAMEA	,                  /* 환자번호, 이름름 */
    OCM01SYSDAT	, OCM01SYSTM	                   /* 날짜, 시간 */                              /* 이미지파일명 */
from OCMPTN01;

select * from all_tables;


