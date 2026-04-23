import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/features/features.csv")

X = df.drop(columns=["churned"])
y = df["churned"]

cat = ["contract_type"]
num = [c for c in X.columns if c not in cat]
print(f"Categorical features: {cat}")
preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(drop="first"), cat),
    ("num", "passthrough", num)
])
print("Preprocessing pipeline created with the following transformations:")
print("- OneHotEncoding for categorical features")
print("- Passthrough for numerical features")
model = Pipeline([
    ("prep", preprocess),
    ("rf", RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=20,
        random_state=42
    ))
])
print("Model pipeline created with RandomForestClassifier:")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.25
)
print(f"Training set size: {X_train.shape[0]} samples")
model.fit(X_train, y_train)
print("Model training completed.")
Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/churn_model.pkl")
print("Model saved to models/churn_model.pkl")