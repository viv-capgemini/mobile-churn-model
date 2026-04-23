import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

print("Loading features...")
df = pd.read_csv("data/features/features.csv")
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

X = df.drop(columns=["churned"])
y = df["churned"]

categorical_features = ["contract_type"]
numeric_features = [c for c in X.columns if c not in categorical_features]

preprocess = ColumnTransformer(
    [
        ("cat", OneHotEncoder(drop="first"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

model = Pipeline(
    [
        ("prep", preprocess),
        (
            "rf",
            RandomForestClassifier(
                n_estimators=300, max_depth=10, min_samples_leaf=20, random_state=42
            ),
        ),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)
print(f"Train: {len(X_train)} samples, Test: {len(X_test)} samples")

print("Training model...")
model.fit(X_train, y_train)
print(f"Training accuracy: {model.score(X_train, y_train):.4f}")
print(f"Test accuracy: {model.score(X_test, y_test):.4f}")

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/churn_model.pkl")
print("Model saved to models/churn_model.pkl")
