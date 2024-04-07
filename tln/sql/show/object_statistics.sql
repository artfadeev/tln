-- Get relations where a concept acts as an object
-- Arguments: :id -- id of the concept
select relations.relation, count(subj.id) as count
from relations
    join concepts as subj on (relations.subject = subj.id)
where relations.object = :id
group by relations.relation
order by relations.relation
