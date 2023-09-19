create table transfers (
    tx_hash VARCHAR(66), 
    address VARCHAR(45),
    token_id bigint,
    src VARCHAR(45),
    dst VARCHAR(45),
    ether numeric(38, 18), 
    weth numeric(38, 18), 
    blur numeric(38, 18), 
    time_updated bigint   
);