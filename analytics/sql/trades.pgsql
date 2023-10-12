create table trades (
    address VARCHAR(45),
    src VARCHAR(45), 
    dst VARCHAR(45), 
    token_id bigint,
    price VARCHAR(100),  -- 100 digit integers
    tx_hash VARCHAR(66),
    market_place VARCHAR(100),
    time_updated timestamp  
);