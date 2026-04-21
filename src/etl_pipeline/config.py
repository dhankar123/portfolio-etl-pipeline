from dataclasses import dataclass
from os import getenv
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    raw_input_path: Path = Path("data/raw/sales_raw.csv")
    curated_output_path: Path = Path("data/curated/sales_curated.csv")
    metadata_output_path: Path = Path("data/curated/pipeline_run_metadata.json")
    log_path: Path = Path("logs/pipeline.log")
    enable_postgres_load: bool = getenv("ENABLE_POSTGRES_LOAD", "false").lower() == "true"
    postgres_url: str = getenv(
        "POSTGRES_URL",
        "postgresql+psycopg://etl_user:etl_password@localhost:5432/etl_db",
    )
    postgres_table_name: str = getenv("POSTGRES_TABLE_NAME", "sales_curated")
