from pathlib import Path

import pandas as pd


def extract_sales_data(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Raw input file not found: {input_path}")
    return pd.read_csv(input_path)
