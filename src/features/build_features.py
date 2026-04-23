import pandas as pd
from pathlib import Path

raw = Path("data/raw/customers.csv")
out = Path("data/features")
out.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw)

df['avg_monthly_spend'] = df['total_charges'] / df['tenure_months']
df['short_tenure'] = (df['tenure_months'] < 6).astype(int)
df['high_support'] = (df['num_support_calls'] >= 4).astype(int)

df.to_csv(out / "features.csv", index=False)
