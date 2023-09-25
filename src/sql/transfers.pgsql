create table transfers (
    tx_hash VARCHAR(66), 
    address VARCHAR(45),
    src VARCHAR(45),
    dst VARCHAR(45),
    token_id bigint,
    time_updated bigint   
);