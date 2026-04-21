FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY data /app/data

RUN pip install --no-cache-dir -e ".[dev]"

CMD ["python", "-m", "etl_pipeline.pipeline"]
