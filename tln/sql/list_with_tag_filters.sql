-- List entries tagged by given set of tags and filtered by label substring
-- Arguments: :query - query for full-text case-insensitive search in label
--            Table selected_tags(tag_id) should contain tags for filtering

-- Computer number of tags for filtering
with selected_tags_number as (
    select count(distinct tag_id) from selected_tags
),
-- For each selected tag, find all its subtags
filter_tags (child_tag, parent_tag) as (
    select tag_id as child_tag, tag_id as parent_tag 
    from selected_tags
    union
    select relations.subject as child_tag, filter_tags.parent_tag as parent_tag
    from relations join filter_tags on (relations.relation='subtag_of' and relations.object=filter_tags.child_tag)
),
-- Find ids of concepts matching those tags
tagged_concepts (id) as (
    select concepts.id as id
    from concepts
        left join relations on (relations.relation='tagged' and concepts.id = relations.subject)
        left join filter_tags on (relations.object = filter_tags.child_tag)
    group by id
    having count(distinct filter_tags.parent_tag) = (select * from selected_tags_number)
)
select note.timestamp, note.label, group_concat(tag.label, ', ') as tags
from tagged_concepts
    left join concepts as note using(id)
    left join relations on (note.id=relations.subject and relations.relation='tagged')
    left join concepts as tag on relations.object = tag.id
group by note.id
having instr(lower(note.label), :query)
order by note.timestamp asc
