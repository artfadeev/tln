create temp table list_results(
    id          text,
    foreign key(id) references concepts(id)
);

insert into list_results
with recursive initial_paths(subject, path, object, present) as (
    select relations_query.object as subject, 'is' as path, relations_query.object, relations_query.present
    from relations_query
),
paths as (
select * from initial_paths
union
select relations.subject, folds.result as path, paths.object, paths.present
from paths
    join folds on paths.path = folds.path
    join relations on relations.relation = folds.next and relations.object = paths.subject
),
relevant_paths as (
select distinct paths.*
from paths join relations_query as q
    on paths.path = q.relation and paths.object=q.object and paths.present=q.present
),
substringed_concepts as (
    select concepts.id, concepts.timestamp, concepts.label
    from concepts
        left join substring_query as q
    group by concepts.id
    having coalesce(sum(instr(lower(concepts.label), q.query)>0),0) = (select count(*) from substring_query)
),
relations_ids(id) as (
select concepts.id
from substringed_concepts as concepts
    left join (select * from relevant_paths where present) as relevant_paths
    on concepts.id=relevant_paths.subject
group by concepts.id
having coalesce(sum(present),0) == (select coalesce(sum(present),0) from relations_query)
except
    select subject
    from relevant_paths
    where not present
)
select id from relations_ids
