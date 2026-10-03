from pathlib import Path

import pandas as pd

from src.quality.checks import (
    check_delivered_orders,
    check_order_ids,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "olist_orders_dataset.csv"


def main():
    orders_df = pd.read_csv(DATA_PATH)

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        orders_df[column] = pd.to_datetime(orders_df[column])

    results = [
        check_delivered_orders(orders_df),
        check_order_ids(orders_df),
    ]

    pipeline_passed = True

    for result in results:
        if result["passed"]:
            print(
                "PASS:",
                result["check"],
            )
        else:
            print(
                "FAIL:",
                result["check"],
                "| Failed records:",
                result["failed_records"],
            )
            pipeline_passed = False

    print("Pipeline passed:", pipeline_passed)


if __name__ == "__main__":
    main()
