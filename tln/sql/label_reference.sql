-- Get id of a concept by its label
-- Arguments: :label - label's text
select id
from concepts
where lower(concepts.label) == :label  

