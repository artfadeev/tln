-- Find concept by label's case-sensitive substring
-- Arguments: :substring - substring
select id
from concepts
where instr(label, :substring)>0
