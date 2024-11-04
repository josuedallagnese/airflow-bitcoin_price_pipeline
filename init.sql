CREATE TABLE IF NOT EXISTS bitcoin_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    usd_rate NUMERIC(12, 2),
    gbp_rate NUMERIC(12, 2),
    eur_rate NUMERIC(12, 2)
);