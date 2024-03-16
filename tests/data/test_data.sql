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

create table marks (
    name            text,
    value           text,

    primary key (name),
    foreign key (value) references concepts(id)
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

insert into relation_t values ('tagged'), ('subtag_of'), ('is');
insert into concepts values ('tln/is_tag', null, 'tag');
insert into relations values ('tln/is_tag', 'tagged', 'tln/is_tag');
insert into folds (next, path, result) values
    ('tagged', 'is', 'tagged'),
    ('subtag_of', 'is', 'subtag_of'),
    ('tagged', 'subtag_of', 'tagged'),
    ('subtag_of', 'subtag_of', 'subtag_of');


-- Test data
insert into concepts values
    ('capital_of_uk', '2000-01-01 12:34:12', 'London is the capital of Great Britain'),
    ('moscow_fact', '2005-02-28 00:15:30', 'Moscow is the largest city in Russia'),
    ('cool_park', '1999-12-31 23:59:59', 'Central Park is a very famous park worth visiting'),
    ('space_travel', '2020-03-01 10:20:30', 'todo: go into space'),
    ('unrelated_fact', '2021-01-02 12:32:22', 'Panda bears may be dangerous'),
    ('vacation2012', '2012-08-30 01:01:01', 'I visited Spain'),
    ('vacation2014', '2014-07-15 02:02:02', 'i visited Spain'),

    ('tag_london', null, 'london'),
    ('tag_moscow', null, 'moscow'),
    ('tag_manhattan', null, 'manhattan'),
    ('tag_newyork', null, 'new_york'),
    ('tag_usa', null, 'usa'),
    ('tag_country', null, 'country'),
    ('tag_china', null, 'china'),
    ('tag_travel', null, 'travel'),
    ('tag_city', null, 'city');

insert into relations values 
    ('capital_of_uk', 'tagged', 'tag_london'),
    ('moscow_fact', 'tagged', 'tag_moscow'),
    ('cool_park', 'tagged', 'tag_manhattan'),
    ('cool_park', 'tagged', 'tag_travel'),
    ('space_travel', 'tagged', 'tag_travel'),
    ('unrelated_fact', 'tagged', 'tag_china'),

    ('tag_london', 'tagged', 'tln/is_tag'),
    ('tag_moscow', 'tagged', 'tln/is_tag'),
    ('tag_manhattan', 'tagged', 'tln/is_tag'),
    ('tag_newyork', 'tagged', 'tln/is_tag'),
    ('tag_usa', 'tagged', 'tln/is_tag'),
    ('tag_country', 'tagged', 'tln/is_tag'),
    ('tag_china', 'tagged', 'tln/is_tag'),
    ('tag_travel', 'tagged', 'tln/is_tag'),
    ('tag_city', 'tagged', 'tln/is_tag'),

    ('tag_manhattan', 'subtag_of', 'tag_newyork'),
    ('tag_newyork', 'subtag_of', 'tag_usa'),

    ('tag_london', 'tagged', 'tag_city'),
    ('tag_moscow', 'tagged', 'tag_city'),
    ('tag_newyork', 'tagged', 'tag_city'),
    ('tag_usa', 'tagged', 'tag_country'),
    ('tag_china','tagged', 'tag_country');

insert into marks values
    ('us', 'tag_usa'),
    ('msk', 'moscow_fact');
