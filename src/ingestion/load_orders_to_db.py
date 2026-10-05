import time
from io import StringIO
from pathlib import Path

import pandas as pd

from src.database.connection import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "olist_orders_dataset.csv"

DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def prepare_orders():
    orders_df = pd.read_csv(DATA_PATH)

    for column in DATE_COLUMNS:
        orders_df[column] = pd.to_datetime(orders_df[column])

    orders_df = orders_df.astype(object).where(
        pd.notna(orders_df),
        None,
    )

    return orders_df


def load_orders():
    orders_df = prepare_orders()

    rows = list(
        orders_df.itertuples(
            index=False,
            name=None,
        )
    )

    start_time = time.perf_counter()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    order_status,
                    order_purchase_timestamp,
                    order_approved_at,
                    order_delivered_carrier_date,
                    order_delivered_customer_date,
                    order_estimated_delivery_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                rows,
            )

    end_time = time.perf_counter()

    print(f"Insert time: {end_time - start_time:.2f} seconds")


def load_orders_copy():
    orders_df = prepare_orders()

    buffer = StringIO()

    orders_df.to_csv(
        buffer,
        index=False,
        header=False,
    )

    start_time = time.perf_counter()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE orders")

            with cursor.copy(
                """
                COPY orders (
                    order_id,
                    customer_id,
                    order_status,
                    order_purchase_timestamp,
                    order_approved_at,
                    order_delivered_carrier_date,
                    order_delivered_customer_date,
                    order_estimated_delivery_date
                )
                FROM STDIN
                WITH (FORMAT CSV)
                """
            ) as copy:
                copy.write(buffer.getvalue())

    end_time = time.perf_counter()

    print(f"COPY insert time: {end_time - start_time:.2f} seconds")
    print("CSV generated in memory")
    print("Buffer size:", len(buffer.getvalue()))


if __name__ == "__main__":
    load_orders_copy()