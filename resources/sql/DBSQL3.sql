-- 가나다
select * from jain_ocs.OCMILL10 where rownum < 100;

select * from ALL_TAB_COMMENTS where TABLE_NAME = 'EMIHDGDC';

select * from ALL_TAB_COMMENTS where OWNER = 'JAIN_OCS' order by comments;
