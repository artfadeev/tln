-- Get ids of concepts matching prefix
-- Arguments: :prefix, :allow_whitespace
select id, label
from concepts
where (:allow_whitespace or instr(id, ' ')==0)
    and instr(id, :prefix) == 1 -- case sensitive
