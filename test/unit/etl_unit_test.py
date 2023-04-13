from constants import default_num_of_customers, default_num_of_orders
from etl.run_etl import (
    generate_customers_data,
    extract_data,
    generate_orders_data,
    transform_data,
)


def test_generate_customers_data():
    assert len(generate_customers_data()) == default_num_of_customers


def test_generate_orders_data():
    assert len(generate_orders_data()) == default_num_of_orders


def test_extract_data():
    assert len(extract_data(num_of_orders=100)[1]) == 100
    assert len(extract_data(num_of_orders=100)[0]) == default_num_of_customers


def test_transform_data():
    customers_data, orders_data = extract_data(500, 10)
    assert len(transform_data(customers_data, orders_data)) == len(orders_data)
