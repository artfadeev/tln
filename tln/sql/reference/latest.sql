-- Select latest concept
select id
from concepts
where timestamp is not null
order by timestamp desc
limit 1
