create temp table relations_query(
    relation    text,
    object      text,
    present     integer,

    foreign key (relation) references relation_t(relation),
    foreign key (object) references concepts(id)
);

create temp table substring_query(
    query       text
);
