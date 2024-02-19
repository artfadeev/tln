-- Tag a concept
-- Arguments: :concept - concept id
--            :tag - tag id
insert into relations(subject, relation, object)
    values (:concept, 'tagged', :tag)
