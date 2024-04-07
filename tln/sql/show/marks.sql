-- Get marks of a given concept
-- Arguments: :id — id of the concept
select marks.name 
from marks
where marks.value = :id
