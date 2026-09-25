"""Train a model and save it unsafely (for RCE flag testing)."""
import pickle
import torch
import torch.nn as nn
import joblib
from sklearn.linear_model import LogisticRegression
import numpy as np

# Train sklearn model
model = LogisticRegression()
model.fit(np.random.randn(100, 10), np.random.randint(0, 2, 100))

# UNSAFE save / load roundtrip
with open("models/classifier.pkl", "wb") as f:
    pickle.dump(model, f)  # flagged on dump side too in some checks

loaded = joblib.load("models/size_model.joblib")  # Flag: joblib_load
