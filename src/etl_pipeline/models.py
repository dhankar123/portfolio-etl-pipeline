from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineMetrics:
    rows_extracted: int
    rows_transformed: int
    rows_loaded: int
