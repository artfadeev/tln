-- Get names of marks starting with given prefix
-- Arguments: :prefix, :allow_whitespace
select name, concepts.label
from marks
    join concepts on (marks.value = concepts.id)
where (:allow_whitespace or instr(name, ' ')==0)
    and instr(name, :prefix) == 1 -- case sensitive
