def check_delivered_orders(orders_df):
    delivered_without_delivery_date = orders_df.loc[
        (orders_df["order_status"] == "delivered")
        & (orders_df["order_delivered_customer_date"].isna())
    ]

    if not delivered_without_delivery_date.empty:
        return {
            "passed": False,
            "check": "delivered_orders_have_delivery_date",
            "failed_records": len(delivered_without_delivery_date),
        }

    return {
        "passed": True,
        "check": "delivered_orders_have_delivery_date",
        "failed_records": 0,
    }


def check_order_ids(orders_df):
    order_ids_na = orders_df["order_id"].isna().sum()

    if order_ids_na > 0:
        return {
            "passed": False,
            "check": "order_id_not_null",
            "failed_records": order_ids_na,
        }

    return {
        "passed": True,
        "check": "order_id_not_null",
        "failed_records": 0,
    }
