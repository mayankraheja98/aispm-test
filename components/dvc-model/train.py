"""DVC-managed training script for return-prediction model."""
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/processed/returns.csv")
X, y = df.drop("returned", axis=1), df["returned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=200, n_jobs=-1)
model.fit(X_train, y_train)
joblib.dump(model, "models/return_predictor.joblib")

metrics = {"accuracy": model.score(X_test, y_test)}
with open("metrics.json", "w") as f:
    json.dump(metrics, f)
