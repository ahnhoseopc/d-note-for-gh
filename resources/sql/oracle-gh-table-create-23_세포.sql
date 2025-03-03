-- JAIN_OCS.SAPCYT08(세포검사결과)

DROP TABLE JAIN_OCS.SAPCYT08 ;

CREATE TABLE "JAIN_OCS"."SAPCYT08" 
   (	"SAP08STATUS" CHAR(2), 
	"SAP08IDNOA" CHAR(7), 
	"SAP08IDNOB" CHAR(1), 
	"SAP08LWDAT" CHAR(8), 
	"SAP08IOCD" CHAR(1), 

	"SAP08ODRDAT" CHAR(8), 
	"SAP08ODRNO" NUMBER(5,0), 
	"SAP08SLPNO" CHAR(3), 
	"SAP08PTLGNO" CHAR(15), 
	"SAP08RSTDAT" CHAR(8), 
	"SAP08RSTTIM" CHAR(8), 

	"SAP08DIAG_BK" VARCHAR2(4000), 
	"SAP08NOTE" VARCHAR2(4000), 
	"SAP08SPTH" CHAR(6), 
	"SAP08DOCCD" CHAR(6), 
	"SAP08SPMNO" VARCHAR2(12), 

	"SAP08RSTYN" CHAR(1) DEFAULT 'N', 
	"SAP08SNDYN" CHAR(1) DEFAULT 'N', 
	"SAP08SAMPLE" VARCHAR2(100), 
	"SAP08COLOR" VARCHAR2(20), 
	"SAP08STA" VARCHAR2(10), 

	"SAP08SUBNO" NUMBER(3,0), 
	"SAP08CODINGDAT" VARCHAR2(30), 
	"SAP08QCCD" VARCHAR2(5), 
	"SAP08QCID" VARCHAR2(6), 
	"SAP08DIAG" CLOB, 

	"SAP08CPART" VARCHAR2(1), 
	"SAP08CDIAG" VARCHAR2(2), 
	"SAP08REMARK" VARCHAR2(1000), 
	"SAP08OTSRTSTDAT" VARCHAR2(8), 
	 CONSTRAINT "INX_SAPCYT080" PRIMARY KEY ("SAP08IDNOA", "SAP08IDNOB", "SAP08LWDAT", "SAP08ODRDAT", "SAP08ODRNO", "SAP08SLPNO", "SAP08SPMNO")
   ) ;

   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08STATUS" IS 'STATUS';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08IDNOA" IS '환자번호';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08IDNOB" IS '타급종구분';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08LWDAT" IS '래원일';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08IOCD" IS '입외구분';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08ODRDAT" IS '오더일';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08ODRNO" IS '오더번호';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08SLPNO" IS '전표번호';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08PTLGNO" IS '미사용';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08RSTDAT" IS '검사완료일';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08RSTTIM" IS '검사완료시간';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08DIAG_BK" IS 'Diagnosis';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08NOTE" IS 'NOTE';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08SPTH" IS '판독의';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08DOCCD" IS '의사코드';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08SPMNO" IS '샘플번호';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08RSTYN" IS '결과유무';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08SNDYN" IS '사인유무';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08SAMPLE" IS '검체';
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08COLOR" IS '검체색깔'; 
   COMMENT ON COLUMN "JAIN_OCS"."SAPCYT08"."SAP08STA" IS '분류코드'; 
   COMMENT ON TABLE "JAIN_OCS"."SAPCYT08"  IS 'CYTOLOGY(2)'; 

INSERT INTO "JAIN_OCS"."SAPCYT08" (SAP08STATUS, SAP08IDNOA, SAP08IDNOB, SAP08LWDAT, SAP08IOCD, 
                                   SAP08ODRDAT, SAP08ODRNO, SAP08SLPNO, SAP08PTLGNO, SAP08RSTDAT, SAP08RSTTIM, 
                                   SAP08DIAG_BK, SAP08NOTE, SAP08SPTH, SAP08DOCCD, SAP08SPMNO, 
                                   SAP08RSTYN, SAP08SNDYN, SAP08SAMPLE, SAP08COLOR, SAP08STA, 
                                   SAP08SUBNO, SAP08CODINGDAT, SAP08QCCD, SAP08QCID, SAP08DIAG, 
                                   SAP08CPART, SAP08CDIAG, SAP08REMARK, SAP08OTSRTSTDAT)
VALUES ('AA', '1234567', '1', '20231027', 'I', 
        '20231027', 1, '001', '123456789012345', '20231027', '100000', 
        '정상 세포 소견', '추적 관찰 필요', 'AA1234', 'AB1234', 'S0000000001', 
        'N', 'N', '검체', '검체색깔', '분류코드', 
        1, '20231027', 'QCCD', 'QCID', 'DIAG', 
        'C', 'CD', 'REMARK', 'OTSRTSTD');

INSERT INTO "JAIN_OCS"."SAPCYT08" (SAP08STATUS, SAP08IDNOA, SAP08IDNOB, SAP08LWDAT, SAP08IOCD, SAP08ODRDAT, SAP08ODRNO, SAP08SLPNO, SAP08PTLGNO, SAP08RSTDAT, SAP08RSTTIM, SAP08DIAG_BK, SAP08NOTE, SAP08SPTH, SAP08DOCCD, SAP08SPMNO, SAP08RSTYN, SAP08SNDYN, SAP08SAMPLE, SAP08COLOR, SAP08STA, SAP08SUBNO, SAP08CODINGDAT, SAP08QCCD, SAP08QCID, SAP08DIAG, SAP08CPART, SAP08CDIAG, SAP08REMARK, SAP08OTSRTSTDAT)
VALUES ('BB', '8765432', '2', '20231028', 'O', '20231028', 2, '002', '123456789012345', '20231028', '110000', '비정형 세포 발견', '추가 검사 필요', 'BB1234', 'BC1234','S0000000002', 'N', 'N', '검체', '검체색깔', '분류코드', 2, '20231028', 'QCCD', 'QCID', 'DIAG', 'C', 'CD', 'REMARK', 'OTSRTSTD');
INSERT INTO "JAIN_OCS"."SAPCYT08" (SAP08STATUS, SAP08IDNOA, SAP08IDNOB, SAP08LWDAT, SAP08IOCD, SAP08ODRDAT, SAP08ODRNO, SAP08SLPNO, SAP08PTLGNO, SAP08RSTDAT, SAP08RSTTIM, SAP08DIAG_BK, SAP08NOTE, SAP08SPTH, SAP08DOCCD, SAP08SPMNO, SAP08RSTYN, SAP08SNDYN, SAP08SAMPLE, SAP08COLOR, SAP08STA, SAP08SUBNO, SAP08CODINGDAT, SAP08QCCD, SAP08QCID, SAP08DIAG, SAP08CPART, SAP08CDIAG, SAP08REMARK, SAP08OTSRTSTDAT)
VALUES ('CC', '1827364', '3', '20231029', 'I', '20231029', 3, '003', '123456789012345', '20231029', '120000', '악성 세포 의심', '즉시 조직 검사 필요', 'CC1234', 'CD1234', 'S0000000003', 'N', 'N', '검체', '검체색깔', '분류코드', 3, '20231029', 'QCCD', 'QCID', 'DIAG', 'C', 'CD', 'REMARK', 'OTSRTSTD');
INSERT INTO "JAIN_OCS"."SAPCYT08" (SAP08STATUS, SAP08IDNOA, SAP08IDNOB, SAP08LWDAT, SAP08IOCD, SAP08ODRDAT, SAP08ODRNO, SAP08SLPNO, SAP08PTLGNO, SAP08RSTDAT, SAP08RSTTIM, SAP08DIAG_BK, SAP08NOTE, SAP08SPTH, SAP08DOCCD, SAP08SPMNO, SAP08RSTYN, SAP08SNDYN, SAP08SAMPLE, SAP08COLOR, SAP08STA, SAP08SUBNO, SAP08CODINGDAT, SAP08QCCD, SAP08QCID, SAP08DIAG, SAP08CPART, SAP08CDIAG, SAP08REMARK, SAP08OTSRTSTDAT)
VALUES ('DD', '2736451', '4', '20231030', 'O', '20231030', 4, '004', '123456789012345', '20231030', '130000', '염증 소견', '약물 치료 필요', 'DD1234', 'DE1234', 'S0000000004', 'N', 'N', '검체', '검체색깔', '분류코드', 4, '20231030', 'QCCD', 'QCID', 'DIAG', 'C', 'CD', 'REMARK', 'OTSRTSTD');
INSERT INTO "JAIN_OCS"."SAPCYT08" (SAP08STATUS, SAP08IDNOA, SAP08IDNOB, SAP08LWDAT, SAP08IOCD, SAP08ODRDAT, SAP08ODRNO, SAP08SLPNO, SAP08PTLGNO, SAP08RSTDAT, SAP08RSTTIM, SAP08DIAG_BK, SAP08NOTE, SAP08SPTH, SAP08DOCCD, SAP08SPMNO, SAP08RSTYN, SAP08SNDYN, SAP08SAMPLE, SAP08COLOR, SAP08STA, SAP08SUBNO, SAP08CODINGDAT, SAP08QCCD, SAP08QCID, SAP08DIAG, SAP08CPART, SAP08CDIAG, SAP08REMARK, SAP08OTSRTSTDAT)
VALUES ('EE', '3645182', '5', '20231031', 'I', '20231031', 5, '005', '123456789012345', '20231031', '140000', '정상 소견', '특이 사항 없음', 'EE1234', 'EF1234', 'S0000000005', 'N', 'N', '검체', '검체색깔', '분류코드', 5, '20231031', 'QCCD', 'QCID', 'DIAG', 'C', 'CD', 'REMARK', 'OTSRTSTD');

COMMIT;

select		
	SAP08STATUS	,
	SAP08IDNOA	,
	SAP08IDNOB	,
	SAP08LWDAT	,
	SAP08IOCD	,
	SAP08ODRDAT	,
	SAP08ODRNO	,
	SAP08SLPNO	,
	SAP08PTLGNO	,
	SAP08RSTDAT	,
	SAP08RSTTIM	,
	SAP08DIAG_BK	,
	SAP08NOTE	,
	SAP08SPTH	,
	SAP08DOCCD	,
	SAP08SPMNO	,
	SAP08RSTYN	,
	SAP08SNDYN	,
	SAP08SAMPLE	,
	SAP08COLOR	,
	SAP08STA	,
	SAP08SUBNO	,
	SAP08CODINGDAT	,
	SAP08QCCD	,
	SAP08QCID	,
	SAP08DIAG	,
	SAP08CPART	,
	SAP08CDIAG	,
	SAP08REMARK	,
	SAP08OTSRTSTDAT	
from JAIN_OCS.SAPCYT08 ;		
------------------------------------------------------------
DROP TABLE JAIN_OCS.SAPCYT07 ;

CREATE TABLE JAIN_OCS.SAPCYT07 (
SAP07STATUS CHAR(2 BYTE) NULL, -- STATUS
SAP07IDNOA CHAR(7 BYTE) NOT NULL, -- 환자번호
SAP07IDNOB CHAR(1 BYTE) NOT NULL, -- 타급종구분
SAP07LWDAT CHAR(8 BYTE) NOT NULL, -- 래원일
SAP07IOCD CHAR(1 BYTE) NULL, -- 입외구분
SAP07ODRDAT CHAR(8 BYTE) NOT NULL, -- 오더일
SAP07ODRNO NUMBER(5) NOT NULL, -- 오더번호
SAP07SLPNO CHAR(3 BYTE) NOT NULL, -- 전표번호
SAP07PTLGNO CHAR(15 BYTE) NULL, -- 미사용
SAP07RSTDAT CHAR(8 BYTE) NULL, -- 검사완료일
SAP07RSTTIM CHAR(8 BYTE) NULL, -- 검사완료시간
SAP07INTP VARCHAR2(4000 BYTE) NULL, -- Cytologic Interpretation
SAP07RCMT VARCHAR2(4000 BYTE) NULL, -- Recommendation
SAP07SPTH CHAR(6 BYTE) NULL, -- 판독의
SAP07DOCCD CHAR(6 BYTE) NULL, -- 예비판독의
SAP07SPMNO VARCHAR2(12 BYTE) NOT NULL, -- 샘플번호
SAP07RSTYN CHAR(1 BYTE) DEFAULT 'N' NULL, -- 결과유무
SAP07SNDYN CHAR(1 BYTE) DEFAULT 'N' NULL, -- 사인유뮤
SAP07SUBNO NUMBER(3) NULL --
);

ALTER TABLE JAIN_OCS.SAPCYT07 ADD CONSTRAINT PK_SAPCYT07
PRIMARY KEY (SAP07IDNOA, SAP07IDNOB, SAP07LWDAT, SAP07ODRDAT, SAP07ODRNO, SAP07SLPNO, SAP07SPMNO);

INSERT INTO JAIN_OCS.SAPCYT07 (SAP07STATUS, SAP07IDNOA, SAP07IDNOB, SAP07LWDAT, SAP07IOCD, SAP07ODRDAT, SAP07ODRNO, SAP07SLPNO, SAP07RSTDAT, SAP07RSTTIM, SAP07INTP, SAP07RCMT, SAP07SPTH, SAP07SPMNO)
VALUES ('AA', '1234567', '1', '20231027', 'I', '20231027', 1, '001', '20231027', '100000', '정상 세포 소견', '추적 관찰 필요', 'AA1234', 'S0000000001');

INSERT INTO JAIN_OCS.SAPCYT07 (SAP07STATUS, SAP07IDNOA, SAP07IDNOB, SAP07LWDAT, SAP07IOCD, SAP07ODRDAT, SAP07ODRNO, SAP07SLPNO, SAP07RSTDAT, SAP07RSTTIM, SAP07INTP, SAP07RCMT, SAP07SPTH, SAP07SPMNO)
VALUES ('BB', '8765432', '2', '20231028', 'O', '20231028', 2, '002', '20231028', '110000', '비정형 세포 발견', '추가 검사 필요', 'BB1234', 'S0000000002');

INSERT INTO JAIN_OCS.SAPCYT07 (SAP07STATUS, SAP07IDNOA, SAP07IDNOB, SAP07LWDAT, SAP07IOCD, SAP07ODRDAT, SAP07ODRNO, SAP07SLPNO, SAP07RSTDAT, SAP07RSTTIM, SAP07INTP, SAP07RCMT, SAP07SPTH, SAP07SPMNO)
VALUES ('CC', '1827364', '3', '20231029', 'I', '20231029', 3, '003', '20231029', '120000', '악성 세포 의심', '즉시 조직 검사 필요', 'CC1234', 'S0000000003');

INSERT INTO JAIN_OCS.SAPCYT07 (SAP07STATUS, SAP07IDNOA, SAP07IDNOB, SAP07LWDAT, SAP07IOCD, SAP07ODRDAT, SAP07ODRNO, SAP07SLPNO, SAP07RSTDAT, SAP07RSTTIM, SAP07INTP, SAP07RCMT, SAP07SPTH, SAP07SPMNO)
VALUES ('DD', '2736451', '4', '20231030', 'O', '20231030', 4, '004', '20231030', '130000', '염증 소견', '약물 치료 필요', 'DD1234', 'S0000000004');

INSERT INTO JAIN_OCS.SAPCYT07 (SAP07STATUS, SAP07IDNOA, SAP07IDNOB, SAP07LWDAT, SAP07IOCD, SAP07ODRDAT, SAP07ODRNO, SAP07SLPNO, SAP07RSTDAT, SAP07RSTTIM, SAP07INTP, SAP07RCMT, SAP07SPTH, SAP07SPMNO)
VALUES ('EE', '3645182', '5', '20231031', 'I', '20231031', 5, '005', '20231031', '140000', '정상 소견', '특이 사항 없음', 'EE1234', 'S0000000005');

COMMIT;

SELECT
SAP07STATUS -- STATUS
, SAP07IDNOA -- 환자번호
, SAP07IDNOB -- 타급종구분
, SAP07LWDAT -- 래원일
, SAP07IOCD -- 입외구분
, SAP07ODRDAT -- 오더일
, SAP07ODRNO -- 오더번호
, SAP07SLPNO -- 전표번호
, SAP07PTLGNO -- 미사용
, SAP07RSTDAT -- 검사완료일
, SAP07RSTTIM -- 검사완료시간
, SAP07INTP -- Cytologic Interpretation
, SAP07RCMT -- Recommendation
, SAP07SPTH -- 판독의
, SAP07DOCCD -- 예비판독의
, SAP07SPMNO -- 샘플번호
, SAP07RSTYN -- 결과유무
, SAP07SNDYN -- 사인유뮤
, SAP07SUBNO --
FROM JAIN_OCS.SAPCYT07;
