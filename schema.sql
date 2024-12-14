SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    price DOUBLE PRECISION,
    pe_ratio DOUBLE PRECISION,
    market_cap BIGINT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL
);

CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL
);

CREATE TABLE portfolio_stocks (
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    stock_id INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (portfolio_id, stock_id)
);

CREATE TABLE stock_transactions (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    stock_id INTEGER NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    purchase_price NUMERIC(10,2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(id),
    stock_id INTEGER NOT NULL REFERENCES stocks(id),
    transaction_type VARCHAR(10) CHECK (transaction_type IN ('buy', 'sell')),
    quantity NUMERIC CHECK (quantity > 0),
    price_per_share NUMERIC CHECK (price_per_share > 0),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
