CREATE extension if NOT EXISTS "uuid-ossp";

CREATE table IF NOT EXISTS btc_moving_avg(
    window_start    TIMESTAMP NOT NULL,
    window_end      TIMESTAMP NOT NULL,
    ticker          VARCHAR(20) NOT NULL,
    avg_price       DOUBLE PRECISION NOT NULL,
    ticks           BIGINT NOT NULL,
    inserted_at     TIMESTAMP DEFAULT NOW()
)
