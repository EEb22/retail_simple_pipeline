DROP SCHEMA IF EXISTS app;
CREATE SCHEMA app;
DROP TABLE IF EXISTS app.flat_orders;
CREATE TABLE app.flat_orders (
    order_id INT,
    customer_id INT,
    first_name varchar(50),
	last_name varchar(50),
	state varchar(50),
	category varchar(50),
	sub_category varchar(50),
	PRIMARY KEY (order_id)
);