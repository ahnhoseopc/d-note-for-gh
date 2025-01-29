select * from all_tables_t where owner = 'JAIN_OCS' order by table_name;
select OWNER, COUNT(TABLE_NAME) from all_tables_t GROUP BY OWNER ORDER  BY OWNER;

select * from ALL_TAB_COMMENTS where owner = 'JAIN_OCS' order by table_name;
select * from ALL_TAB_COMMENTS where owner = 'JAIN_ORD' order by table_name;

select * from ALL_COL_COMMENTS CC
where CC.owner = 'JAIN_OCS' and CC.COMMENTS like '%진단%' order by table_name;

SELECT TC.TABLE_NAME, TC.COMMENTS, CC.COLUMN_NAME, CC.COMMENTS
FROM ALL_COL_COMMENTS CC
INNER JOIN ALL_TAB_COMMENTS TC ON CC.OWNER = TC.OWNER AND CC.TABLE_NAME = TC.TABLE_NAME
WHERE CC.OWNER = 'JAIN_OCS' AND CC.COMMENTS LIKE '%병%'
ORDER BY CC.TABLE_NAME, CC.COLUMN_NAME;

/*
JAIN_ORD.ORDIDN01_DAMO
JAIN_OCS.OEYIPD04  입원 Order
JAIN_OCS.SAPILL10  소견병명
JAIN_OCS.OMTILL06  과별병명코드
*/

select * from JAIN_OCS.OEYIPD04 where rownum < 100 order by OEY04ODRDAT DESC;

select * from JAIN_OCS.SAPILL10 where rownum < 100 ;
select * from JAIN_OCS.SAPILL32 where rownum < 100 ;