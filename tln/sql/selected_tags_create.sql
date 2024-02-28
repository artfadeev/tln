-- Create temporary table of selected tags for filtering
-- Arguments: none
create temp table selected_tags (
    tag_id      string,
    foreign key (tag_id) references concepts(id)
);
