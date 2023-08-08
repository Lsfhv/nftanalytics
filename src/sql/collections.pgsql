-- Define collections table.

create table collections (
    address VARCHAR(45) primary key, 
    slug VARCHAR(200) unique not null, -- collection name
    chain VARCHAR(200) not null,
    floor numeric, 
    total_listed int, 
    total_supply int, -- How many nfts in a collection
    last_updated bigint not null -- epoch time when it was last updated
);