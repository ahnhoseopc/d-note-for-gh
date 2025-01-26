select * from jain_ocs.OMTCST20;
select * from jain_ocs.OMTCST41;
select * from jain_ocs.WM$OMTCST14;
select * from jain_ocs.SRD$OMTCST14;


select * from all_tab_comments where COMMENTS like '%프로토콜%';
select * from all_col_comments where COMMENTS like '%전표ID%';

select * from jain_hc.hc_ptlmst;
select * from jain_ocs.OMTCMT24;

select omt24status, count(1) from jain_ocs.OMTCMT24 group by omt24status;


SELECT
  OMT24SPTH -- 코드
, OMT24CODE -- 코드
, OMT24CODENM -- 코드명
, OMT24CMT -- 손견
, OMT24CMTB --
FROM JAIN_OCS.OMTCMT24
WHERE ROWNUM < 100
AND OMT24KWA = 'GY'
AND (OMT24SPTH = '001607' OR OMT24SPTH = '999999')
AND OMT24SLPID = 'OPR'
ORDER BY OMT24KWA , OMT24SPTH DESC, OMT24CODE;

SELECT
  OMT24KWA -- 코드
, OMT24SPTH -- 코드
, OMT24CODE -- 코드
, OMT24CODENM -- 코드명
, OMT24CMT -- 손견
, OMT24CMTB --
FROM JAIN_OCS.OMTCMT24
WHERE ROWNUM < 100
--AND OMT24KWA = 'GS'
--AND (OMT24SPTH = '001607' OR OMT24SPTH = '999999')
AND OMT24SLPID = 'OPR'
AND OMT24CMT like '%specimen%'
ORDER BY OMT24KWA , OMT24SPTH DESC, OMT24CODE;

select * from jain_ocs.OCMOPR06
where ocm06opdat = '20241017' 
AND ocm06cmta like '%단순%';

/*
1. specimen 
Rt.lobe(permanent Bx.의뢰함)
2.LN dissection : 
D&P node (permanent Bx. 의뢰함)
Rt.level VI LN (permanent Bx. 의뢰함)
3. parathyroid : Rt.sup.,inf. parathyroid were preserved
Lt.sup.,inf. parathyroid were preserved
4. Strap muscle invasion(-)
5. Trachea invasion/capsule invasion(-/-)
6. Recurrent laryngeal N/surounding structure (intact/intact)
7. Q block 1.5g/hemoblock/Megaderm/tacoseal/veraseal 2 4ml/Megashield 3cc

@1. The patient was placed in comfortable supine position
2. The 6cm sized incision was done by 15 knife
3. The plastysma m. was divided with the cutting cautery.
4. The strap m. are separated.
5. The thyroid lobe(Rt.) was exposed by mobilizing the strap m.(sternohyoid and sternothyroid m.)
6. The middle vein was exposed, divided, and ligated.
7. Baccock clamps were applied to inferior and superior aspects of the thyroid lobe(Rt.&Lt.) to facilitate medical retraciting on the gland
8. Superior pole vessels were divided individually, and then ligated without external laryngeal nerve and vocal cord injury.
9. A gentle dissection with Hoyt clamp was used to exposure the parathyroid gland, inferior thyroid a. and recurrent laryngeal n.
10. The branches of the inferior thyroid artery were divided at the surface of the thyroid gland
11. The inferior thyroid vein was ligated and divided
12. The dissection of thyroid from the trachea was performed with cautery by division of loose connective tissue.
13. After identifying the parathyroid gland, inferior artery and recurrent laryngeal n. thr thyroid was divided so that the isthmus included in the specimen.
14. Barovac 100cc was inserted. After indenification of no bleeding, fascia and skin was closed with vicryl 3-0 and vicryl 4-0, PDS 5-0, silk 6-0, skin stapler ,allevyn thin 10*10.

EBL : 30cc/a little
sponge count correct? yes

*/