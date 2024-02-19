-- Mark a concept
-- Arguments: :concept - concept id
--            :mark - mark name (without leading dot)
insert into marks(name, value)
    values (:mark, :concept)
