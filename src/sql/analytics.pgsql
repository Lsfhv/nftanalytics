-- Define analytics table.

create table analytics (
    address VARCHAR(45) not null, 
    floor numeric, 
    total_listed int, 
    tlpm int,
    tlpH int, 
    tlp6H int,
    tlp12H int,
    tlpD int,
    tlpW int,
    last_updated bigint not null -- epoch time when it was last updated
);