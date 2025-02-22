with op as (
select 
    ocm06idnoa,ocm06lwdat, ocm06opdat, ocm06seqno,
    substr(ocm06cmta, 1, instr(ocm06cmta, '|', 1, 1)-1) cmta01spth,
    substr(ocm06cmta, instr(ocm06cmta, '|', 1, 8)+1, instr(ocm06cmta, '|', 1,  9)-instr(ocm06cmta, '|', 1, 8)-1) cmta08opname,
    substr(ocm06cmta, instr(ocm06cmta, '|', 1,10)+1, instr(ocm06cmta, '|', 1, 11)-instr(ocm06cmta, '|', 1,10)-1) cmta10,
    substr(ocm06cmta, instr(ocm06cmta, '|', 1, 9)+1, instr(ocm06cmta, '|', 1, 10)-instr(ocm06cmta, '|', 1, 9)-1) cmta09oproom,
    substr(ocm06cmta, instr(ocm06cmta, '|', 1, 7)+1, instr(ocm06cmta, '|', 1,  8)-instr(ocm06cmta, '|', 1, 7)-1) cmta07predx,
    substr(ocm06cmta, instr(ocm06cmta, '|', 1,11)+1, instr(ocm06cmta, '|', 1, 12)-instr(ocm06cmta, '|', 1,11)-1) cmta11postdx,
    ocm06cmtb,
    ocm06memo
from jain_ocs.ocmopr06 
where ocm06status = 'OP2'
and rownum < 1000
)
select * from op
where cmta10 is not null
order by ocm06lwdat DESC;
