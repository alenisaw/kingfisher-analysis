-- Создание таблицы products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для оптимизации запросов по категории
CREATE INDEX IF NOT EXISTS idx_category ON products(category);
-- Создание индекса для оптимизации запросов по цене
CREATE INDEX IF NOT EXISTS idx_price ON products(price);
