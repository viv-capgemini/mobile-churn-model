import joblib
import pandas as pd
from fastapi import FastAPI
from api.schemas import CustomerInput, ChurnPrediction

MODEL_PATH = "models/churn_model.pkl"

app = FastAPI(
    title="Telco Churn Prediction API",
    description="Predict customer churn probability",
    version="1.0.0"
)

# Load model once at startup
model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=ChurnPrediction)
def predict_churn(customer: CustomerInput):
    data = pd.DataFrame([customer.dict()])

    # Feature engineering (must match training)
    data['avg_monthly_spend'] = data['total_charges'] / data['tenure_months']
    data['short_tenure'] = (data['tenure_months'] < 6).astype(int)
    data['high_support'] = (data['num_support_calls'] >= 4).astype(int)
    data['young_customer'] = (data['age'] < 25).astype(int)
    data['senior_customer'] = (data['age'] >= 65).astype(int)

    churn_prob = model.predict_proba(data)[0][1]
    churn_label = int(churn_prob >= 0.5)

    return ChurnPrediction(
        churn_probability=round(churn_prob, 4),
        churn_label=churn_label
    )
