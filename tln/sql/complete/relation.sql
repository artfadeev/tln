-- Complete relation name
-- Arguments: :prefix
select relation
from relation_t
    where instr(relation, :prefix) == 1
