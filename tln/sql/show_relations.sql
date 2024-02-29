-- Get relations where a concept acts as a subject 
-- Arguments: :id -- id of the object
select relations.relation, obj.id, obj.label
from relations
    join concepts as obj on (relations.object = obj.id)
where relations.subject = :id
order by relations.relation
