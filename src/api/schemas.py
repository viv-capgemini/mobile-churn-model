from pydantic import BaseModel, Field
from typing import Literal

class CustomerInput(BaseModel):
    age: int = Field(..., ge=18, le=85)
    contract_type: Literal['Phone+SIM', 'SIM-only', 'Rolling']
    tenure_months: int = Field(..., ge=1)
    monthly_charges: float = Field(..., ge=0)
    device_cost: float = Field(..., ge=0)
    num_support_calls: int = Field(..., ge=0)
    total_charges: float = Field(..., ge=0)

class ChurnPrediction(BaseModel):
    churn_probability: float
    churn_label: int