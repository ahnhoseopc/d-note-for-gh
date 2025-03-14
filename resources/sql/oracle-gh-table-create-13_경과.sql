-- JAIN_OCS.ODRCMT03(경과기록지)

DROP TABLE JAIN_OCS.ODRCMT03 ;

CREATE TABLE JAIN_OCS.ODRCMT03 (	
ODR03STATUS CHAR(2 BYTE) NULL, -- STATUS	
ODR03IDNOA CHAR(7 BYTE) NOT NULL, -- 환자번호	
ODR03IDNOB CHAR(1 BYTE) NOT NULL, -- 타급종구분	
ODR03LWDAT CHAR(8 BYTE) NOT NULL, -- 래원/입원일	
ODR03KWA CHAR(2 BYTE) NOT NULL, -- 과	
ODR03SPTH CHAR(6 BYTE) NOT NULL, -- 의사	
ODR03IOCD CHAR(1 BYTE) NULL, -- I/O구분 I : 입원경과기록지 O: 외래경과기록지	
ODR03ODRDAT CHAR(8 BYTE) NOT NULL, -- 작성일	
ODR03ODRNO NUMBER(5) NOT NULL, --	
ODR03SUBNO NUMBER(3) NOT NULL, --	
ODR03ODRDV CHAR(2 BYTE) NULL, --	
ODR03CMTDV CHAR(2 BYTE) NOT NULL, --	
ODR03ODRCMT VARCHAR2(4000 BYTE) NULL, -- 내용	
ODR03SYSTM VARCHAR2(100 BYTE) NULL, -- 최초저장시간	
ODR03ODRCMT02 VARCHAR2(4000 BYTE) NULL, --	
ODR03ODRCMT03 VARCHAR2(4000 BYTE) NULL, --	
ODR03ODRCMT04 VARCHAR2(4000 BYTE) NULL, --	
ODR03ODRCMT05 VARCHAR2(4000 BYTE) NULL, --	
ODR03SYSDAT VARCHAR2(8 BYTE) NULL, -- 최초저장일자	
ODR03WSNM VARCHAR2(15 BYTE) NULL, --	
ODR03EXMPTXT CLOB NULL, --	
ODR03EXMP CLOB NULL --	
);	

ALTER TABLE JAIN_OCS.ODRCMT03 ADD CONSTRAINT PK_ODRCMT03
PRIMARY KEY (ODR03IDNOA, ODR03IDNOB, ODR03LWDAT, ODR03ODRDAT, ODR03KWA, ODR03SPTH, ODR03CMTDV, ODR03ODRNO, ODR03SUBNO);

INSERT INTO JAIN_OCS.ODRCMT03 (ODR03STATUS, ODR03IDNOA, ODR03IDNOB, ODR03LWDAT, ODR03KWA, ODR03SPTH, ODR03IOCD, ODR03ODRDAT, ODR03ODRNO, ODR03SUBNO, ODR03ODRDV, ODR03CMTDV, ODR03ODRCMT, ODR03SYSTM, ODR03SYSDAT, ODR03WSNM)
VALUES ('AA', '1234567', '1', '20231027', 'AA', 'AA1234', 'I', '20231027', 1, 1, 'AA', 'AA', '환자 상태 양호', '100000', '20231027', '홍길동');

INSERT INTO JAIN_OCS.ODRCMT03 (ODR03STATUS, ODR03IDNOA, ODR03IDNOB, ODR03LWDAT, ODR03KWA, ODR03SPTH, ODR03IOCD, ODR03ODRDAT, ODR03ODRNO, ODR03SUBNO, ODR03ODRDV, ODR03CMTDV, ODR03ODRCMT, ODR03SYSTM, ODR03SYSDAT, ODR03WSNM)
VALUES ('BB', '8765432', '2', '20231028', 'BB', 'BB1234', 'O', '20231028', 2, 1, 'BB', 'BB', '환자 상태 호전 중', '110000', '20231028', '김철수');

INSERT INTO JAIN_OCS.ODRCMT03 (ODR03STATUS, ODR03IDNOA, ODR03IDNOB, ODR03LWDAT, ODR03KWA, ODR03SPTH, ODR03IOCD, ODR03ODRDAT, ODR03ODRNO, ODR03SUBNO, ODR03ODRDV, ODR03CMTDV, ODR03ODRCMT, ODR03SYSTM, ODR03SYSDAT, ODR03WSNM)
VALUES ('CC', '1827364', '3', '20231029', 'CC', 'CC1234', 'I', '20231029', 3, 1, 'CC', 'CC', '환자 상태 악화', '120000', '20231029', '박영희');

INSERT INTO JAIN_OCS.ODRCMT03 (ODR03STATUS, ODR03IDNOA, ODR03IDNOB, ODR03LWDAT, ODR03KWA, ODR03SPTH, ODR03IOCD, ODR03ODRDAT, ODR03ODRNO, ODR03SUBNO, ODR03ODRDV, ODR03CMTDV, ODR03ODRCMT, ODR03SYSTM, ODR03SYSDAT, ODR03WSNM)
VALUES ('DD', '2736451', '4', '20231030', 'DD', 'DD1234', 'O', '20231030', 4, 1, 'DD', 'DD', '환자 상태 보통', '130000', '20231030', '최순이');

INSERT INTO JAIN_OCS.ODRCMT03 (ODR03STATUS, ODR03IDNOA, ODR03IDNOB, ODR03LWDAT, ODR03KWA, ODR03SPTH, ODR03IOCD, ODR03ODRDAT, ODR03ODRNO, ODR03SUBNO, ODR03ODRDV, ODR03CMTDV, ODR03ODRCMT, ODR03SYSTM, ODR03SYSDAT, ODR03WSNM)
VALUES ('EE', '3645182', '5', '20231031', 'EE', 'EE1234', 'I', '20231031', 5, 1, 'EE', 'EE', '환자 상태 불안정', '140000', '20231031', '강감찬');

COMMIT;

SELECT
ODR03STATUS -- STATUS
, ODR03IDNOA -- 환자번호
, ODR03IDNOB -- 타급종구분
, ODR03LWDAT -- 래원/입원일
, ODR03KWA -- 과
, ODR03SPTH -- 의사
, ODR03IOCD -- I/O구분 I : 입원경과기록지 O: 외래경과기록지
, ODR03ODRDAT -- 작성일
, ODR03ODRNO --
, ODR03SUBNO --
, ODR03ODRDV --
, ODR03CMTDV --
, ODR03ODRCMT -- 내용
, ODR03SYSTM -- 최초저장시간
, ODR03ODRCMT02 --
, ODR03ODRCMT03 --
, ODR03ODRCMT04 --
, ODR03ODRCMT05 --
, ODR03SYSDAT -- 최초저장일자
, ODR03WSNM --
, ODR03EXMPTXT --
, ODR03EXMP --
FROM JAIN_OCS.ODRCMT03;