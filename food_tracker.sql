-- A table for storing tracked dates
create table date_log (
    id integer primary key autoincrement,
    date_log date not null
);


-- A table for storing foods data
create table food (
    id integer primary key autoincrement,
    name text not null,
    protein integer not null,
    carbohydrates integer not null,
    fat integer not null,
    calories integer not null
);


-- A table for storing the relationship between a date and its foods
create table date_food (
    date_log_id integer not null,
    food_id integer not null,
    primary key (date_log_id, food_id)
);
