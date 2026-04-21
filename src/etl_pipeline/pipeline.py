import logging

from etl_pipeline.config import PipelineConfig
from etl_pipeline.extract import extract_sales_data
from etl_pipeline.load import load_curated_data, write_run_metadata
from etl_pipeline.logging_config import configure_logging
from etl_pipeline.models import PipelineMetrics
from etl_pipeline.transform import transform_sales_data

logger = logging.getLogger(__name__)


def run_pipeline(config: PipelineConfig | None = None) -> PipelineMetrics:
    resolved_config = config or PipelineConfig()
    configure_logging(resolved_config.log_path)
    logger.info("Starting ETL pipeline run")

    raw_df = extract_sales_data(resolved_config.raw_input_path)
    logger.info("Extract completed with %s rows", len(raw_df))

    curated_df = transform_sales_data(raw_df)
    logger.info("Transform completed with %s rows", len(curated_df))

    loaded_count = load_curated_data(curated_df, resolved_config.curated_output_path)
    metrics = PipelineMetrics(
        rows_extracted=len(raw_df),
        rows_transformed=len(curated_df),
        rows_loaded=loaded_count,
    )
    write_run_metadata(metrics, resolved_config.metadata_output_path)
    logger.info("Load completed with %s rows", loaded_count)
    logger.info("ETL pipeline run finished successfully")
    return metrics


if __name__ == "__main__":
    run_pipeline()
