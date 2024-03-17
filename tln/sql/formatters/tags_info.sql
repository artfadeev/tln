select tags.id, tags.label, count(tagged.subject) as directly_tagged
from list_results
    join concepts as tags using(id)
    left join relations as tagged
        on tags.id==tagged.object and tagged.relation='tagged'
group by tags.id, tags.label
