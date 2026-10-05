import pandas as pd

from src.quality.checks import (
    check_delivered_orders,
    check_order_ids,
)

#FAIL TESTS

def test_delivered_order_without_delivery_date_fails():
    orders_df = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_status": ["delivered"],
            "order_delivered_customer_date": [pd.NaT],
        }
    )

    result = check_delivered_orders(orders_df)

    assert result["passed"] is False
    assert result["failed_records"] == 1


def test_order_id_not_null():
    orders_df = pd.DataFrame(
        {
            "order_id": [None],
        }
    )

    result = check_order_ids(orders_df)

    assert result["passed"] is False
    assert result["failed_records"] == 1

#PASS TESTS

def test_delivered_order_with_delivery_date_passes():
    orders_df = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_status": ["delivered"],
            "order_delivered_customer_date": [
                pd.Timestamp("2018-01-01")
            ],
        }
    )

    result = check_delivered_orders(orders_df)

    assert result["passed"] is True
    assert result["failed_records"] == 0


def test_order_id_not_null_passes():
    orders_df = pd.DataFrame(
        {
            "order_id": ["order-1"],
        }
    )

    result = check_order_ids(orders_df)

    assert result["passed"] is True
    assert result["failed_records"] == 0
