from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    raw_input_path: Path = Path("data/raw/sales_raw.csv")
    curated_output_path: Path = Path("data/curated/sales_curated.csv")
    metadata_output_path: Path = Path("data/curated/pipeline_run_metadata.json")
    log_path: Path = Path("logs/pipeline.log")
