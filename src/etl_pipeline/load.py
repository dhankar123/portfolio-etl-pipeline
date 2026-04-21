import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from etl_pipeline.models import PipelineMetrics


def load_curated_data(df: pd.DataFrame, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return len(df)


def load_curated_data_to_postgres(df: pd.DataFrame, postgres_url: str, table_name: str) -> int:
    engine = create_engine(postgres_url)
    with engine.begin() as connection:
        df.to_sql(name=table_name, con=connection, if_exists="replace", index=False)
    return len(df)


def write_run_metadata(metrics: PipelineMetrics, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "pipeline_name": "portfolio_simple_etl",
        "run_timestamp_utc": datetime.now(UTC).isoformat(),
        "metrics": {
            "rows_extracted": metrics.rows_extracted,
            "rows_transformed": metrics.rows_transformed,
            "rows_loaded": metrics.rows_loaded,
        },
    }

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
