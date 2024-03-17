-- Select latest concept
-- Arguments: :offset
select id
from concepts
where timestamp is not null
order by timestamp desc
limit 1
offset :offset
