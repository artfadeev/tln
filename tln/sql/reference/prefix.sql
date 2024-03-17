-- Find concept by label's case-sensitive prefix
-- Arguments: :prefix - prefix of the label
select id
from concepts
where instr(label, :prefix)==1
