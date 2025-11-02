# Project Workflow — News Sentiment Analysis

## Overview
This document describes the end-to-end project workflow for the News Sentiment Analysis repository. It contains:

- A Mermaid workflow diagram showing components and data flow.
- Technical details mapping each component to repository files.
- Data model and DB layout used by `MongoDBHandler`.
- Environment, setup, and run instructions for Windows/PowerShell.
- Tests, quality gates, and verification steps.
- Scaling notes (Spark) and operational recommendations.

---

## Mermaid Workflow Diagram

```mermaid
flowchart TD
  subgraph Collect
    A[News Collector\n(`news_collector.py`)] --> B[Preprocessor\n(`sentiment_analyzer.py` / preprocessing)]
  end

  subgraph Analyze
    B --> C[Sentiment Analyzer\n(`sentiment_analyzer.py`) ]
    C --> D[Scoring & Consensus\n(VADER, TextBlob, custom)]
  end

  subgraph Store
    D --> E[MongoDB (`mongodb_handler.py`)]
  end

  subgraph Visualize
    E --> F[Dashboard (`dashboard.py` / `visualizer.py` / Streamlit)]
    F --> G[Output Charts & CSVs (`output/`)]
  end

  subgraph Orchestration
    M[Main / Runner\n(`main.py`, `run.bat`, `run.ps1`)] --> A
    M --> F
  end

  subgraph Scaling
    B -->|Large data| S[Pyspark Jobs\n(`spark_repro.py`, `spark_smoke.py`)]
    S --> D
  end

  E -.->|Metrics & Stats| H[Monitoring & Alerts]

  style A fill:#f9f,stroke:#333,stroke-width:1px
  style C fill:#ffefba,stroke:#333
  style E fill:#bfefff,stroke:#333
  style F fill:#d5f5e3,stroke:#333
```
```

---

## High-level components & repo mapping

- Data collection
  - `news_collector.py` — fetches articles from NewsAPI (or other sources). Uses `NEWS_API_KEY` and `NEWS_API_BASE_URL` from `config.py`.

- Preprocessing & analysis
  - `sentiment_analyzer.py` — text cleaning, tokenization, and running multiple sentiment analyzers (VADER, TextBlob, or model-based). Produces fields such as `sentiment`, `sentiment_score`, `vader_compound`, `textblob_polarity`.

- Persistence
  - `mongodb_handler.py` — wraps MongoDB access. Uses `config.MONGODB_URI`, `config.MONGODB_DB` (default: `news_sentiment_db`), and `config.MONGODB_COLLECTION` (default: `news_articles`).
  - Key methods: `insert_articles(df)`, `get_all_articles(limit)`, `get_articles_by_sentiment(sentiment)`, `get_articles_by_source(source)`, `get_statistics()`.

- Visualization / Dashboard
  - `dashboard.py` — Streamlit dashboard entrypoint.
  - `visualizer.py` — helper functions to build charts (Plotly/Altair/matplotlib as available).
  - Output directory: `output/` (created by `config.create_output_directory()` if missing).

- Orchestration / runners
  - `main.py` — high-level pipeline runner used for scheduled/one-shot runs.
  - `run.bat`, `run.ps1`, `run_dashboard.bat` — convenience scripts for Windows.

- Spark support
  - `spark_repro.py`, `spark_smoke.py`, `spark_compatibility_note.md` — helper scripts for scaling processing with PySpark.

- Tests
  - `test_setup.py`, `test_full_pipeline.py`, `test_spark_dataframe.py` — unit/integration tests.

- Configuration
  - `config.py` — centralized settings and defaults. Loads environment variables via `python-dotenv`.

---

## Data model (document example)
MongoDB documents inserted by `MongoDBHandler.insert_articles()` typically include (inferred from code and pipeline):

- _id (ObjectId, converted to string when returned)
- title (string)
- description / summary (string)
- content (string)
- url (string)
- source (string)
- published_at (datetime)
- sentiment (string) — e.g. `Positive`, `Neutral`, `Negative`
- sentiment_score (float) — aggregated score used to decide label
- vader_compound (float)
- textblob_polarity (float)
- inserted_at (datetime) — timestamp when document is inserted

Note: `insert_articles` normalizes pandas/NumPy types and sets `None` for NaN values.

---

## Configuration (.env template)
Create a `.env` file in the project root with at least the following keys:

```
NEWS_API_KEY=your_newsapi_key_here
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster0.example.mongodb.net
# Optional overrides
MONGODB_DB=news_sentiment_db
MONGODB_COLLECTION=news_articles
```

`config.py` also exposes Spark and dashboard defaults (SPARK_MASTER, DASHBOARD_PORT, etc.).

---

## Environment & Setup (Windows / PowerShell)

1) Create and activate a Python virtual environment (Python 3.11 recommended — repository contains `venv311/`):

```powershell
# from project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# or if using the provided venv311, activate that instead:
# .\venv311\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3) Create `.env` as shown above.

4) Validate config

```powershell
python -c "import config; config.validate_config()"
```

---

## Run the pipeline

- Quick (one-shot) run (main pipeline):

```powershell
# from project root
python main.py
# or use the provided script
.\run.bat
# or
.\run.ps1
```

- Run the dashboard (Streamlit):

```powershell
# default: port from config.DASHBOARD_PORT (8501)
python dashboard.py
# or use convenience script
.\run_dashboard.bat
```

Notes: `dashboard.py` likely runs a Streamlit app; if not, it will start whatever server is implemented.

---

## Tests & Quality Gates

Run the test suite with pytest:

```powershell
pip install pytest
pytest -q
```

Suggested quick quality checks prior to commit:
- Linting (flake8 / pylint) — add if desired.
- Run unit tests in `test_setup.py` and `test_spark_dataframe.py`.
- Smoke test: `python run_quick_test.py` (exists in repo).

Quick triage guidance (local):
- Build: no compiled build step required — PASS if venv and deps install successfully.
- Lint/Typecheck: run linters (not present by default) — optional.
- Tests: run `pytest` — expected to pass if environment and external services (NewsAPI/Mongo) are available.

---

## Scaling, Spark, and performance

- The codebase includes `spark_repro.py` and `spark_smoke.py` for using PySpark when processing large datasets. `config.SPARK_MASTER` defaults to `local[1]` for Windows compatibility; change to `local[*]` or a cluster URL for production.
- When scaling:
  - Increase `SPARK_DRIVER_MEMORY` and `SPARK_EXECUTOR_MEMORY` in `config.py`.
  - Use `SPARK_PARTITIONS` to tune parallelism.
  - Prefer writing intermediate aggregated results to a file store (Parquet) before heavy joins.

---

## Monitoring & operational notes

- Database metrics: use `MongoDBHandler.get_statistics()` to compute ingestion and sentiment distributions. Send those metrics to a monitoring system (Prometheus/Grafana) by exporting totals on a schedule.
- Backups: export `news_articles` collection regularly (mongodump / scheduled job).
- Secrets: store `MONGODB_URI` and `NEWS_API_KEY` in a secure secret store for production (Azure Key Vault, AWS Secrets Manager).

---

## Verification checklist (post-deploy)

- [ ] `.env` has valid `NEWS_API_KEY` and `MONGODB_URI`.
- [ ] `python main.py` completes a run and `mongodb_handler` shows non-zero `total_articles`.
- [ ] Dashboard loads and shows charts.
- [ ] Unit tests pass: `pytest -q`.

---

## Next steps & improvements

- Add CI workflow (GitHub Actions) to run tests and lint on PRs.
- Add a Dockerfile and docker-compose that runs a test MongoDB and the app for reproducible dev environments.
- Add type hints and mypy for stronger type checking.
- Add integration tests that mock NewsAPI and use a local MongoDB instance (or ephemeral test containers).

---

## Files created/edited

- `PROJECT_WORKFLOW.md` — this file: contains the workflow diagram and technical details.

---

## Short completion summary
This document captures the project's architecture, data flow, run instructions, and operational notes. Use it as the canonical reference for onboarding, CI, and deployment planning.
