-- Complete 
-- Arguments: :prefix, :allow_whitespace
select substr(label, instr(lower(label), :prefix)) as label_suffix, label
from concepts
where (:allow_whitespace or instr(label, ' ') == 0)
    and instr(lower(label), :prefix)
