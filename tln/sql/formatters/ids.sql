select id
from list_results
    join concepts using(id)
order by timestamp asc
