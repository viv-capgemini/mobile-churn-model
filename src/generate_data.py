import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
n_samples = 5000
output_path = Path("data/raw")
output_path.mkdir(parents=True, exist_ok=True)

# --- NEW: realistic age distribution ---
ages = np.clip(
    np.random.normal(loc=42, scale=12, size=n_samples),
    18, 85
).astype(int)

contract_types = np.random.choice(
    ['Phone+SIM', 'SIM-only', 'Rolling'],
    size=n_samples,
    p=[0.48, 0.32, 0.20]
)

tenure = []
monthly = []
device_cost = []

for c in contract_types:
    if c == 'Phone+SIM':
        tenure.append(np.random.randint(12, 61))
        monthly.append(np.random.uniform(45, 95))
        device_cost.append(np.random.uniform(600, 1200))
    elif c == 'SIM-only':
        tenure.append(np.random.randint(1, 37))
        monthly.append(np.random.uniform(8, 35))
        device_cost.append(0)
    else:  # Rolling
        tenure.append(np.random.randint(1, 13))
        monthly.append(np.random.uniform(15, 45))
        device_cost.append(0)

tenure = np.array(tenure)
monthly = np.array(monthly)
support_calls = np.random.poisson(2, n_samples)

# Churn logic (age has weak but realistic effect)
churn_prob = (
    0.12
    + (contract_types == 'Rolling') * 0.20
    + (tenure < 6) * 0.15
    + (support_calls >= 4) * 0.20
    + (ages < 25) * 0.05     # younger customers churn slightly more
)

churn = np.random.binomial(1, np.clip(churn_prob, 0, 0.85))

df = pd.DataFrame({
    "age": ages,                         # ✅ NEW
    "contract_type": contract_types,
    "tenure_months": tenure,
    "monthly_charges": monthly,
    "device_cost": device_cost,
    "num_support_calls": support_calls,
    "total_charges": tenure * monthly,
    "churned": churn
})

df.to_csv(output_path / "customers.csv", index=False)
