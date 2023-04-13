import random
from typing import Dict, List, Optional

from faker import Faker

from constants import (
    categories,
    default_num_of_customers,
    default_num_of_orders,
    states,
    sub_categories,
)
from src.etl.utils.config import get_warehouse_creds
from src.etl.utils.db import WarehouseConnection

import psycopg2.extras as p


def generate_customers_data(
    num_of_customers: Optional[int] = None,
) -> List[Dict]:
    # create fake customers:
    # input: declare the number of customers
    # output: list of dictionary: { id, first_name, last_name, state }
    fake = Faker()
    customer_data = []
    if num_of_customers is None:
        num_of_customers = default_num_of_customers

    for i in range(1, num_of_customers + 1):
        customer_data.append(
            {
                "id": i,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "state": random.choice(states),
            }
        )
    return customer_data


def generate_orders_data(
    num_of_orders: Optional[int] = None,
    num_of_customers: Optional[int] = None,
) -> List[Dict]:
    order_data = []

    if num_of_orders is None:
        num_of_orders = default_num_of_orders

    if num_of_customers is None:
        num_of_customers = default_num_of_customers

    for i in range(1, num_of_orders + 1):
        cat = random.choice(categories)
        order_data.append(
            {
                "id": i,
                "customer_id": random.choice(range(1, num_of_customers + 1)),
                "cat": cat,
                "sub_cat": random.choice(sub_categories[cat]),
            }
        )
    return order_data


def extract_data(
    num_of_customers: Optional[int] = None,
    num_of_orders: Optional[int] = None,
) -> List[List]:
    customer_data = generate_customers_data(num_of_customers)
    order_data = generate_orders_data(num_of_orders, num_of_customers)
    return [customer_data, order_data]


def transform_data(
    customer_data: List[Dict], order_data: List[Dict]
) -> List[Dict]:
    # enrich orders_data with customer_data and make a flat table
    # to decrease the time complexity,
    # a hash map has been created for customers_data
    # to find the customers data for the orders faster.
    customer_hash_map = {}
    for i in customer_data:
        customer_hash_map[i["id"]] = i

    flat_data = []
    for o in order_data:
        flat_data.append(
            {
                "order_id": o["id"],
                "customer_id": o["customer_id"],
                "first_name": customer_hash_map[o["customer_id"]][
                    "first_name"
                ],
                "last_name": customer_hash_map[o["customer_id"]]["last_name"],
                "state": customer_hash_map[o["customer_id"]]["state"],
                "category": o["cat"],
                "sub_category": o["sub_cat"],
            }
        )
    return flat_data


def _flat_data_insert_query() -> str:
    return """
    INSERT INTO app.flat_orders (
        order_id,
        customer_id,
        first_name,
        last_name,
        state,
        category,
        sub_category
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    on conflict(order_id)
    do update set
        (customer_id, first_name, last_name, 
        state, category, sub_category) =
        (EXCLUDED.customer_id, EXCLUDED.first_name, EXCLUDED.last_name,
         EXCLUDED.state, EXCLUDED.category, EXCLUDED.sub_category);
    """



def load_data_to_warehouse(data_to_insert: List[Dict]) -> None:
    insert_query = _flat_data_insert_query()
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, insert_query, data_to_insert)



def run():
    # num_orders = #default_num_of_orders
    # num_customers = #default_num_of_customers
    customers_data, orders_data = extract_data()
    flat_order = transform_data(customers_data, orders_data)
    # load_data_to_warehouse(flat_order)
    return flat_order


if __name__ == '__main__':
    run()
