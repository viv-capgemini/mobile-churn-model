# Churn Model MLOps Demo

A demonstration of MLOps practices for a customer churn prediction model.

## What Does This Model Do?

Imagine you run a telecom company with thousands of customers. Some customers are happy and stay for years, while others leave (churn) after a few months. This model predicts which customers are likely to leave.

### Example Customer

Viv is 51 years old, has been a customer for 24 months, pays £39.99/month, and has called support 3 times. The model returns:

```json
{
  "churn_probability": 0.73,
  "churn_label": 1
}
```

Translation: Viv has a 73% chance of canceling. Your business can now offer a discount, reach out with personalised support, or take action before she leaves.

The model uses patterns like:

- High monthly charges → more likely to churn
- More support calls → customer is frustrated
- Low tenure → loyalty not yet established

## Project Structure

```
mobile-churn-model/
├── dvc.yaml                          # DVC pipeline definition
├── requirements.txt                  # Python dependencies
├── data/
│   ├── raw/customers.csv             # Generated synthetic dataset
│   └── features/features.csv        # Engineered features
├── models/
│   └── churn_model.pkl               # Trained model
└── src/
    ├── api/
    │   ├── main.py                   # FastAPI inference server
    │   └── schemas.py                # Request/response schemas
    ├── data/
    │   └── generate_data.py          # Generate synthetic churn dataset
    ├── features/
    │   └── build_features.py         # Feature engineering
    └── train/
        └── train_model.py            # Model training
```

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Pipeline

```bash
# Run all stages (generate data → build features → train model)
dvc repro

# Or run stages individually
python src/data/generate_data.py
python src/features/build_features.py
python src/train/train_model.py
```

## Running the API

```bash
uvicorn api.main:app --app-dir src
# Visit http://localhost:8000/docs
```

### Port already in use

```bash
lsof -ti :8000 | xargs kill -9
```

## API Usage

**`POST /predict`**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 34,
    "contract_type": "SIM-only",
    "tenure_months": 4,
    "monthly_charges": 22.0,
    "device_cost": 0,
    "num_support_calls": 3,
    "total_charges": 88.0
  }'
```

Response:

```json
{
  "churn_probability": 0.67,
  "churn_label": 1
}
```

**`GET /health`**

```bash
curl http://localhost:8000/health
```

Response:

```json
{"status": "ok"}
```

### `contract_type` values

| Value | Description |
|---|---|
| `Phone+SIM` | Handset + SIM contract |
| `SIM-only` | SIM-only plan |
| `Rolling` | Rolling monthly contract |
Response:
```
{
  "churn": 1,
  "churn_probability": 0.73
}
```