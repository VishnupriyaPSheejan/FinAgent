# FinAgent — Financial Time-Series Forecasting & AI Agent Platform

FinAgent is a portfolio-grade foundation for a production-style financial AI engineering platform.

The project starts with a daily transaction-volume forecasting problem and is designed to evolve into a multi-agent system with:

- Time-series forecasting
- Feature engineering
- Anomaly detection
- FastAPI
- Pydantic
- RAG / vector search
- LangGraph orchestration
- MCP / A2A integrations
- AWS deployment
- Docker / Kubernetes / EKS
- Terraform
- CI/CD
- Observability

> **Data note:** The transaction-related data in `data/raw/transactions.csv` is synthetic and created for development/demo purposes. It is not JPMorgan customer data.

## Current implementation

The repository currently includes a working forecasting baseline using:

1. Time-aware train/test splitting
2. Calendar and lag features
3. XGBoost regression
4. MAE, RMSE and MAPE evaluation
5. Model persistence with Joblib
6. FastAPI prediction endpoint
7. Automated tests
8. Docker support
9. GitHub Actions CI

The architecture intentionally leaves clean extension points for the agentic/RAG/AWS layers.

---

## Project structure

```text
FinAgent/
├── .github/
│   └── workflows/
│       └── ci.yml
├── configs/
│   └── config.yaml
├── data/
│   ├── raw/
│   │   └── transactions.csv
│   └── processed/
├── docker/
│   └── Dockerfile
├── notebooks/
│   └── README.md
├── scripts/
│   ├── train.py
│   └── predict.py
├── src/
│   └── finagent/
│       ├── __init__.py
│       ├── config.py
│       ├── data.py
│       ├── evaluation.py
│       ├── features.py
│       ├── model.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── main.py
│       ├── features/
│       │   └── __init__.py
│       └── models/
│           └── __init__.py
├── tests/
│   ├── test_api.py
│   ├── test_features.py
│   └── test_model.py
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/FinAgent.git
cd FinAgent
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

For development tools:

```bash
pip install -r requirements-dev.txt
```

## 4. Train the model

```bash
python scripts/train.py
```

This creates:

```text
models/finagent_xgb.joblib
```

and prints the test metrics.

## 5. Run the API

```bash
uvicorn finagent.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI lets you test the API interactively.

## 6. Run a prediction

After training:

```bash
python scripts/predict.py
```

## 7. Run tests

```bash
pytest
```

---

## API

### Health check

```http
GET /health
```

### Forecast

```http
POST /forecast
```

Example request:

```json
{
  "transaction_volume": 1100000,
  "transaction_value_usd": 55000000,
  "avg_transaction_value": 50,
  "digital_transaction_share": 0.58,
  "international_transaction_share": 0.12,
  "fed_funds_rate": 4.5,
  "inflation_rate": 2.7,
  "unemployment_rate": 4.2,
  "vix": 18,
  "sp500_index": 5200,
  "day_of_week": 2,
  "month": 9,
  "quarter": 3,
  "is_weekend": 0,
  "is_month_end": 0,
  "is_quarter_end": 0,
  "is_holiday": 0,
  "lag_1": 1080000,
  "lag_7": 1040000,
  "rolling_mean_7": 1060000,
  "rolling_std_7": 45000
}
```

---

## Modeling approach

The current target is:

```text
target_next_day_volume
```

The feature pipeline creates:

### Calendar features

- day of week
- month
- quarter
- weekend
- month end
- quarter end
- holiday

### Lag features

- lag 1
- lag 7
- lag 14
- lag 28

### Rolling features

- 7-day mean
- 7-day standard deviation
- 28-day mean
- 28-day standard deviation

### External features

- federal funds rate
- inflation
- unemployment
- VIX
- S&P 500 index

The split is chronological rather than random to avoid time-series leakage.

---

## Roadmap

### Phase 1 — Forecasting foundation

- [x] Data ingestion
- [x] Feature engineering
- [x] Time-aware split
- [x] XGBoost baseline
- [x] Evaluation
- [x] FastAPI
- [x] Pydantic
- [x] Tests
- [x] Docker
- [x] CI

### Phase 2 — Advanced time series

- [ ] Naive baseline
- [ ] Moving average
- [ ] ARIMA/SARIMA
- [ ] LSTM
- [ ] Temporal Fusion Transformer
- [ ] Prediction intervals
- [ ] Backtesting
- [ ] Model registry

### Phase 3 — AI agents

- [ ] LangGraph supervisor
- [ ] Forecast Agent
- [ ] Anomaly Agent
- [ ] Research/RAG Agent
- [ ] Risk Agent
- [ ] Report Agent

### Phase 4 — RAG

- [ ] Document ingestion
- [ ] Chunking
- [ ] Embeddings
- [ ] FAISS/Qdrant
- [ ] Retrieval evaluation
- [ ] Grounded responses

### Phase 5 — Agent protocols

- [ ] MCP server
- [ ] A2A communication
- [ ] Structured Pydantic agent messages
- [ ] Tool authorization

### Phase 6 — AWS

- [ ] S3
- [ ] Lambda
- [ ] ECR
- [ ] EKS
- [ ] Bedrock
- [ ] CloudWatch
- [ ] IAM

### Phase 7 — DevOps

- [x] Docker
- [x] GitHub Actions
- [ ] Terraform
- [ ] Kubernetes manifests
- [ ] Security scanning
- [ ] Automated deployment

### Phase 8 — Observability

- [ ] OpenTelemetry
- [ ] Prometheus
- [ ] Grafana
- [ ] Agent latency
- [ ] Token usage
- [ ] RAG retrieval metrics
- [ ] Model drift monitoring

---

## Data

The included dataset contains approximately 2,800 daily observations.

The transaction data is synthetic. Macro-style variables are included so that the repository can be used immediately without requiring credentials or external APIs.

For a production-style version, replace/enrich the macro features with public economic time series and document the source and licensing terms.

---

## Responsible use

This is an educational/portfolio project. It is not intended for investment advice, financial decision-making, credit decisions, or production banking systems.

Do not upload confidential, proprietary, customer, or regulated financial data.

---

## License

MIT License. See `LICENSE`.
