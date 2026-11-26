USE ecommerce_business_analytics;

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght FLOAT,
    product_description_lenght FLOAT,
    product_photos_qty FLOAT,
    product_weight_g FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT
);

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date VARCHAR(50),
    price DECIMAL(12,2),
    freight_value DECIMAL(12,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

CREATE TABLE payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(30),
    payment_installments INT,
    payment_value DECIMAL(12,2),
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date VARCHAR(50),
    review_answer_timestamp VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat DOUBLE,
    geolocation_lng DOUBLE,
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10)
);

CREATE TABLE category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

USE ecommerce_business_analytics;

SHOW TABLES;
SELECT * FROM customers LIMIT 5;
SELECT COUNT(*) AS total_customers
FROM customers;
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(customer_id IS NULL) AS missing_customer_ids
FROM customers;

SHOW VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE 'local_infile';
SHOW VARIABLES LIKE 'secure_file_priv';
SELECT COUNT(*) FROM customers;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/products_cleaned.csv'
REPLACE INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id, @category, @name_length, @description_length, @photos, @weight, @length, @height, @width)
SET
product_id = @id,
product_category_name = NULLIF(TRIM(@category), ''),
product_name_lenght = NULLIF(REPLACE(TRIM(@name_length), '\r', ''), ''),
product_description_lenght = NULLIF(REPLACE(TRIM(@description_length), '\r', ''), ''),
product_photos_qty = NULLIF(REPLACE(TRIM(@photos), '\r', ''), ''),
product_weight_g = NULLIF(REPLACE(TRIM(@weight), '\r', ''), ''),
product_length_cm = NULLIF(REPLACE(TRIM(@length), '\r', ''), ''),
product_height_cm = NULLIF(REPLACE(TRIM(@height), '\r', ''), ''),
product_width_cm = NULLIF(REPLACE(TRIM(@width), '\r', ''), '');

SELECT COUNT(*) FROM products;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sellers_cleaned.csv'
REPLACE INTO TABLE sellers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id, @zip, @city, @state)
SET
seller_id = @id,
seller_zip_code_prefix = NULLIF(REPLACE(TRIM(@zip), '\r', ''), ''),
seller_city = TRIM(@city),
seller_state = REPLACE(TRIM(@state), '\r', '');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/orders_cleaned.csv'
REPLACE INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@order_id, @customer_id, @status, @purchase, @approved, @carrier, @delivered, @estimated)
SET
order_id = @order_id,
customer_id = @customer_id,
order_status = @status,
order_purchase_timestamp = NULLIF(REPLACE(TRIM(@purchase), '\r', ''), ''),
order_approved_at = NULLIF(REPLACE(TRIM(@approved), '\r', ''), ''),
order_delivered_carrier_date = NULLIF(REPLACE(TRIM(@carrier), '\r', ''), ''),
order_delivered_customer_date = NULLIF(REPLACE(TRIM(@delivered), '\r', ''), ''),
order_estimated_delivery_date = NULLIF(REPLACE(TRIM(@estimated), '\r', ''), '');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/order_items_cleaned.csv'
REPLACE INTO TABLE order_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@order_id, @item_id, @product_id, @seller_id, @shipping, @price, @freight)
SET
order_id = @order_id,
order_item_id = NULLIF(REPLACE(TRIM(@item_id), '\r', ''), ''),
product_id = @product_id,
seller_id = @seller_id,
shipping_limit_date = REPLACE(TRIM(@shipping), '\r', ''),
price = NULLIF(REPLACE(TRIM(@price), '\r', ''), ''),
freight_value = NULLIF(REPLACE(TRIM(@freight), '\r', ''), '');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/payments_cleaned.csv'
REPLACE INTO TABLE payments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@order_id, @sequence, @type, @installments, @value)
SET
order_id = @order_id,
payment_sequential = NULLIF(REPLACE(TRIM(@sequence), '\r', ''), ''),
payment_type = REPLACE(TRIM(@type), '\r', ''),
payment_installments = NULLIF(REPLACE(TRIM(@installments), '\r', ''), ''),
payment_value = NULLIF(REPLACE(TRIM(@value), '\r', ''), '');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/reviews_cleaned.csv'
REPLACE INTO TABLE reviews
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@review_id, @order_id, @score, @title, @message, @creation, @answer)
SET
review_id = @review_id,
order_id = @order_id,
review_score = NULLIF(REPLACE(TRIM(@score), '\r', ''), ''),
review_comment_title = REPLACE(TRIM(@title), '\r', ''),
review_comment_message = REPLACE(TRIM(@message), '\r', ''),
review_creation_date = REPLACE(TRIM(@creation), '\r', ''),
review_answer_timestamp = REPLACE(TRIM(@answer), '\r', '');

SELECT COUNT(*) FROM reviews;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/geolocation_cleaned.csv'
INTO TABLE geolocation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@zip, @lat, @lng, @city, @state)
SET
geolocation_zip_code_prefix = NULLIF(REPLACE(TRIM(@zip), '\r', ''), ''),
geolocation_lat = NULLIF(REPLACE(TRIM(@lat), '\r', ''), ''),
geolocation_lng = NULLIF(REPLACE(TRIM(@lng), '\r', ''), ''),
geolocation_city = TRIM(@city),
geolocation_state = REPLACE(TRIM(@state), '\r', '');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/category_translation_cleaned.csv'
REPLACE INTO TABLE category_translation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@category, @english)
SET
product_category_name = TRIM(@category),
product_category_name_english = REPLACE(TRIM(@english), '\r', '');

SHOW TABLES;
SELECT DATABASE();

SELECT COUNT(*) AS total_orders
FROM orders;
SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers;

SELECT ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;
SELECT ROUND(
    (SELECT SUM(payment_value) FROM payments) /
    (SELECT COUNT(*) FROM orders), 2
) AS average_order_value;

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

SELECT
    p.product_category_name,
    COUNT(*) AS total_items
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_items DESC
LIMIT 10;

SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY order_month
ORDER BY order_month;

SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM reviews;

SELECT
    payment_type,
    COUNT(*) AS total_payments,
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments
GROUP BY payment_type
ORDER BY total_revenue DESC;

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) AS one_time_customers
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) AS customer_orders;

SELECT
    order_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY order_month) AS previous_month_revenue
FROM (
    SELECT
        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,
        ROUND(SUM(p.payment_value), 2) AS monthly_revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY order_month
) AS monthly_sales
ORDER BY order_month;

SELECT
    customer_unique_id,
    order_count
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) AS customer_summary
WHERE order_count > 1
ORDER BY order_count DESC;

SELECT COUNT(*) AS repeat_customer_rows
FROM (
    SELECT c.customer_unique_id
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
    HAVING COUNT(o.order_id) > 1
) AS repeat_customers;

SELECT
    order_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY order_month) AS previous_month_revenue
FROM (
    SELECT
        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,
        ROUND(SUM(p.payment_value), 2) AS monthly_revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY order_month
) AS monthly_sales
ORDER BY order_month;

SELECT COUNT(*) AS total_reviews
FROM reviews;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT review_id) AS unique_review_ids
FROM reviews;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT review_id) AS unique_ids,
    SUM(review_id IS NULL) AS missing_ids
FROM reviews;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(order_id IS NULL) AS missing_order_ids
FROM reviews;