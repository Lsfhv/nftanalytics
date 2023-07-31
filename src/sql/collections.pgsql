-- Define collections table.

create table collections (
    address VARCHAR(45) primary key, 
    slug VARCHAR(200) unique not null, -- collection name
    chain VARCHAR(200),
    floor numeric, 
    total_listed int, 
    total_supply int, -- How many nfts in a collection
    total_listed_in_past_minute int,
    total_listed_in_past_hour int, 
    total_listed_in_past_6hours int,
    total_listed_in_past_12hours int,
    total_listed_in_past_day int,
    total_listed_in_past_week int,
    marketplace VARCHAR(200),
    last_updated bigint not null -- epoch time when it was last updated
);