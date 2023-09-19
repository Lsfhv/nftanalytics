create table transfers (
    address VARCHAR(45) primary key, 
    src VARCHAR(45),
    dst VARCHAR(45),
    ether bigint, 
    weth bigint, 
    blur bigint, 
    time_updated bigint   
);