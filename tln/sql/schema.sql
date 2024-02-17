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

    foreign key (subject) references concepts(id),
    foreign key (relation) references relation_t(relation),
    foreign key (object) references concepts(id)
);

create table folds (
    left_           text,
    right_          text,
    result          text,

    primary key (left_, right_, result),

    foreign key (left_) references relation_t(relation),
    foreign key (right_) references relation_t(relation),
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
insert into folds (left_, right_, result) values
    ('tagged', 'subtag_of', 'tagged'),
    ('subtag_of', 'subtag_of', 'subtag_of');
