select subject, object
from relations
where subject in list_results
    and object in list_results
    and relation='subtag_of'
