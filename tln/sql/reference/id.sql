-- Check that object with given id exists
-- Arguments: :id - id of the concept
select id
from concepts
where id = :id
