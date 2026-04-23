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

categorical_features = ["contract_type"]
numeric_features = [c for c in X.columns if c not in categorical_features]

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(drop="first"), categorical_features),
    ("num", "passthrough", numeric_features)
])

model = Pipeline([
    ("prep", preprocess),
    ("rf", RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=20,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

model.fit(X_train, y_train)

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/churn_model.pkl")