import pandas as pd

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount_pct",
}


def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_cols}")

    clean_df = df.copy()
    clean_df = clean_df.dropna(subset=["order_id", "order_date", "quantity", "unit_price"])

    clean_df["order_date"] = pd.to_datetime(clean_df["order_date"], errors="coerce")
    clean_df = clean_df.dropna(subset=["order_date"])

    clean_df["quantity"] = pd.to_numeric(clean_df["quantity"], errors="coerce")
    clean_df["unit_price"] = pd.to_numeric(clean_df["unit_price"], errors="coerce")
    clean_df["discount_pct"] = pd.to_numeric(clean_df["discount_pct"], errors="coerce").fillna(0.0)

    clean_df = clean_df.dropna(subset=["quantity", "unit_price"])
    clean_df = clean_df[(clean_df["quantity"] > 0) & (clean_df["unit_price"] > 0)]

    clean_df["gross_revenue"] = clean_df["quantity"] * clean_df["unit_price"]
    clean_df["net_revenue"] = clean_df["gross_revenue"] * (1 - clean_df["discount_pct"])

    clean_df["order_date"] = clean_df["order_date"].dt.date.astype(str)
    return clean_df.sort_values(by=["order_date", "order_id"]).reset_index(drop=True)
