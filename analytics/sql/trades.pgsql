create table trades (
    address VARCHAR(45),
    src VARCHAR(45), 
    dst VARCHAR(45), 
    tokenid bigint,
    price VARCHAR(100),  -- 100 digit integers
    txhash VARCHAR(66),
    platform VARCHAR(100),
    timestamp timestamp  
);