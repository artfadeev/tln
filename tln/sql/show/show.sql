-- Get concepts entry by id
-- Arguments: :id - id of the entry
select id, timestamp, label
from concepts
where id = :id
