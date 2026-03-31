CREATE DATABASE ecommerce;
USE ecommerce;
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price FLOAT
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    quantity INT,
    total_amount FLOAT
);

-- Total sales
SELECT SUM(total_amount) FROM order_details;

-- Top products
SELECT product_id, SUM(quantity) AS total_sold
FROM order_details
GROUP BY product_id
ORDER BY total_sold DESC;

-- Monthly sales
SELECT MONTH(order_date), SUM(total_amount)
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
GROUP BY MONTH(order_date);