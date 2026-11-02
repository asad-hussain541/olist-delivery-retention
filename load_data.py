"""Load the raw Olist CSVs into a local SQLite database (data/olist.db).

Run once:  python load_data.py
Source: Olist Brazilian E-Commerce Public Dataset (Kaggle, CC BY-NC-SA 4.0).
Place the 9 CSVs in data/raw/ first (see README for the download link).
"""
from pathlib import Path
import sqlite3

import pandas as pd

RAW = Path("data/raw")
DB = Path("data/olist.db")

# file name -> table name
TABLES = {
    "orders.csv": "orders",
    "order_items.csv": "order_items",
    "customers.csv": "customers",
    "sellers.csv": "sellers",
    "products.csv": "products",
    "payments.csv": "payments",
    "reviews.csv": "reviews",
    "category_name.csv": "category_translation",
}

DATE_COLS = {
    "orders": ["order_purchase_timestamp", "order_approved_at",
               "order_delivered_carrier_date", "order_delivered_customer_date",
               "order_estimated_delivery_date"],
    "order_items": ["shipping_limit_date"],
    "reviews": ["review_creation_date", "review_answer_timestamp"],
}


def main() -> None:
    DB.unlink(missing_ok=True)
    con = sqlite3.connect(DB)
    for file, table in TABLES.items():
        df = pd.read_csv(RAW / file)
        for col in DATE_COLS.get(table, []):
            # store as ISO text so SQLite date functions (julianday, strftime) work
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
        df.to_sql(table, con, index=False)
        print(f"{table:22s} {len(df):>8,} rows")

    # indexes on the join keys keep the analysis queries fast
    for stmt in [
        "CREATE INDEX ix_orders_customer ON orders(customer_id)",
        "CREATE INDEX ix_orders_id ON orders(order_id)",
        "CREATE INDEX ix_items_order ON order_items(order_id)",
        "CREATE INDEX ix_reviews_order ON reviews(order_id)",
        "CREATE INDEX ix_customers_id ON customers(customer_id)",
        "CREATE INDEX ix_customers_unique ON customers(customer_unique_id)",
    ]:
        con.execute(stmt)
    con.commit()
    con.close()
    print(f"\nSaved {DB}")


if __name__ == "__main__":
    main()
