import csv
import datetime
from typing import Dict, List

import psycopg2.extras as p

from etl.run_etl import run
from etl.utils.config import get_warehouse_creds
from etl.utils.db import WarehouseConnection


class TestETL:
    def teardown_method(self, test_integration_etl) -> None:
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("TRUNCATE TABLE app.flat_orders;")

    def get_warehouse_data(self) -> List[Dict]:
        with WarehouseConnection(get_warehouse_creds()).managed_cursor(
            cursor_factory=p.DictCursor
        ) as curr:
            curr.execute(
                """SELECT cast(order_id as varchar),
                        cast(customer_id as varchar),
                        first_name,
                        last_name,
                        state,
                        category,
                        sub_category,
                        cast(order_date as varchar)
                        FROM app.flat_orders;"""
            )
            result = [dict(r) for r in curr.fetchall()]
        return result

    def test_integration_etl(self, mocker):
        mocker.patch(
            "etl.run_etl.extract_data",
            return_value=[
                [
                    r
                    for r in csv.DictReader(
                        open(r"test/fixtures/sample_customers_data.csv")
                    )
                ],
                [
                    r
                    for r in csv.DictReader(
                        open("test/fixtures/sample_orders_data.csv")
                    )
                ],
            ],
        )
        run()

        result = self.get_warehouse_data()
        expected_result = [
            r
            for r in csv.DictReader(
                open(r"test/fixtures/sample_result_data.csv")
            )
        ]

        for item in expected_result:
            item.update({"order_date": "2021-01-01"})

        assert result == expected_result
