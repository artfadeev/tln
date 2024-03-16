select note.timestamp, note.label, group_concat(tag.label, ', ') as tags
from list_results
    left join concepts as note using(id)
    left join relations on (note.id=relations.subject and relations.relation='tagged')
    left join concepts as tag on relations.object = tag.id
group by note.id
order by note.timestamp asc
