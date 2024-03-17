-- Get id of a concept by mark
-- Arguments: :mark - mark name
select value as id
from marks
where name = :mark 
