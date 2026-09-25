"""Train a size recommendation model using sklearn."""
import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

mlflow.set_experiment("size-recommendation")

with mlflow.start_run():
    X = pd.read_csv("data/features.csv")
    y = pd.read_csv("data/labels.csv").values.ravel()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", GradientBoostingClassifier()),
    ])

    param_grid = {"clf__n_estimators": [100, 200], "clf__max_depth": [3, 5]}
    grid = GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1)
    grid.fit(X_train, y_train)

    mlflow.log_params(grid.best_params_)
    mlflow.log_metric("accuracy", grid.score(X_test, y_test))

    joblib.dump(grid.best_estimator_, "models/size_model.joblib")
    mlflow.sklearn.log_model(grid.best_estimator_, "model")
    print("Model saved")
