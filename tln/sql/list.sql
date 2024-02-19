-- Get info about database entries with tags in chronological order 
-- Arguments: :query - query for full-text case-insensitive search
select note.timestamp, note.label, group_concat(tag.label, ', ') as tags
from concepts as note
    left join relations
        on note.id=relations.subject and relations.relation='tagged'
    left join concepts as tag
        on relations.object=tag.id
where instr(lower(note.label), :query)>0
group by note.id
order by note.timestamp asc
