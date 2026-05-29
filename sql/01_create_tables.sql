-- Run this in pgAdmin after creating your database
-- Recommended DB name: retail_db

CREATE TABLE IF NOT EXISTS customers (
    customer_id     VARCHAR(20)  PRIMARY KEY,
    country         VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    stock_code      VARCHAR(20)  PRIMARY KEY,
    description     VARCHAR(255) NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    invoice_no      VARCHAR(20)  PRIMARY KEY,
    customer_id     VARCHAR(20)  REFERENCES customers(customer_id),
    invoice_date    TIMESTAMP    NOT NULL,
    country         VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS sale_items (
    id              SERIAL       PRIMARY KEY,
    invoice_no      VARCHAR(20)  REFERENCES sales(invoice_no),
    stock_code      VARCHAR(20)  REFERENCES products(stock_code),
    quantity        INTEGER      NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL,
    total_price     NUMERIC(10, 2) NOT NULL
);
