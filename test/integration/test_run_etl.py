import csv

from etl.run_etl import run


def test_integration_etl(mocker):
    mocker.patch(
        "etl.run_etl.generate_data",
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
    result = run()
    expected_result = [
        r
        for r in csv.DictReader(open(r"test/fixtures/sample_result_data.csv"))
    ]

    assert result == expected_result
