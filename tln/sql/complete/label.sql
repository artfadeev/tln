-- Complete concept label 
-- Arguments: :prefix, :allow_whitespace
select label
from concepts
where (:allow_whitespace or instr(label, ' ') == 0)
    and instr(lower(label), :prefix) == 1
