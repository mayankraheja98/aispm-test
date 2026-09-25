"""
WARNING: This file demonstrates UNSAFE model loading patterns.
These are flagged by AI-SPM as security risks (pickle RCE, unsafe deserialization).
DO NOT use these patterns in production.
"""
import pickle
import torch
import joblib
import numpy as np

# CRITICAL: pickle.load() — arbitrary code execution risk
# Flag: pickle_load
with open("models/classifier.pkl", "rb") as f:
    sklearn_model = pickle.load(f)  # RCE if model file is tampered

# CRITICAL: torch.load() without weights_only=True — pickle-based, RCE risk
# Flag: torch_load_unsafe
pytorch_model = torch.load("models/fashion_encoder.pt")  # unsafe
pytorch_model_2 = torch.load("checkpoints/best_model.pth")  # also unsafe

# CRITICAL: joblib.load() — similar pickle-based risk
# Flag: joblib_load
size_predictor = joblib.load("models/size_model.joblib")  # RCE risk

# CRITICAL: np.load with allow_pickle=True
feature_store = np.load("data/embeddings.npy", allow_pickle=True)

print("Models loaded (unsafely)")
