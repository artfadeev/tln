drop table if exists concepts;
drop table if exists relation_t;
drop table if exists relations;
drop table if exists folds;
drop table if exists marks;

create table concepts (
    id              text,
    timestamp       timestamp,
    label           text not null,

    primary key (id)
);

create table relation_t (
    relation        text,

    primary key (relation)
);

create table relations (
    subject         text,
    relation        text,
    object          text,

    primary key (subject, relation, object),
    foreign key (subject) references concepts(id),
    foreign key (relation) references relation_t(relation),
    foreign key (object) references concepts(id)
);

create table folds (
    next            text, -- was left_
    path            text, -- was right_
    result          text,

    primary key (next, path, result),

    foreign key (next) references relation_t(relation),
    foreign key (path) references relation_t(relation),
    foreign key (result) references relation_t(relation)
);

create table marks (
    name            text,
    value           text,

    primary key (name),
    foreign key (value) references concepts(id)
);

insert into relation_t values ("tagged"), ("subtag_of"), ("is");
insert into concepts values ("tln/is_tag", null, "tag");
insert into folds (next, path, result) values
    ('tagged', 'is', 'tagged'),
    ('subtag_of', 'is', 'subtag_of'),
    ('tagged', 'subtag_of', 'tagged'),
    ('subtag_of', 'subtag_of', 'subtag_of');
