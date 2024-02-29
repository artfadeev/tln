-- Add new relation between concepts
-- Arguments: :subject, :object -- ids of concepts
--            :relation -- name of relation (one of relation_t)
insert into relations(subject, relation, object)
values (:subject, :relation, :object)
