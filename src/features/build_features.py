import pandas as pd
from pathlib import Path

raw = Path("data/raw/customers.csv")
out = Path("data/features")
out.mkdir(parents=True, exist_ok=True)
print(f"Loading raw data from {raw}...")
df = pd.read_csv(raw)

df['avg_monthly_spend'] = df['total_charges'] / df['tenure_months']
df['short_tenure'] = (df['tenure_months'] < 6).astype(int)
df['high_support'] = (df['num_support_calls'] >= 4).astype(int)
print("Feature engineering completed. Sample of features:")
print(df[['avg_monthly_spend', 'short_tenure', 'high_support']].head())
df.to_csv(out / "features.csv", index=False)
print(f"Features saved to {out / 'features.csv'}")
