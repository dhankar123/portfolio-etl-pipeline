import pandas as pd
import pytest

from etl_pipeline.transform import transform_sales_data


def test_transform_sales_data_derives_revenue_and_filters_invalid_rows() -> None:
    source = pd.DataFrame(
        [
            {
                "order_id": "1",
                "order_date": "2026-04-01",
                "customer_id": "C1",
                "product_id": "P1",
                "quantity": 2,
                "unit_price": 10.0,
                "discount_pct": 0.10,
            },
            {
                "order_id": "2",
                "order_date": "bad-date",
                "customer_id": "C2",
                "product_id": "P2",
                "quantity": 1,
                "unit_price": 20.0,
                "discount_pct": 0.00,
            },
            {
                "order_id": "3",
                "order_date": "2026-04-02",
                "customer_id": "C3",
                "product_id": "P3",
                "quantity": 0,
                "unit_price": 30.0,
                "discount_pct": 0.00,
            },
        ]
    )

    transformed = transform_sales_data(source)

    assert len(transformed) == 1
    assert transformed.iloc[0]["gross_revenue"] == 20.0
    assert transformed.iloc[0]["net_revenue"] == 18.0


def test_transform_sales_data_raises_for_missing_columns() -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        transform_sales_data(pd.DataFrame([{"order_id": "1"}]))
