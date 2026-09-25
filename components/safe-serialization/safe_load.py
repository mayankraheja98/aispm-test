"""Demonstrates SAFE model serialization patterns — no pickle deserialization."""
import torch
from safetensors.torch import load_file, save_file
import onnxruntime as ort

# SAFE: safetensors — no pickle, no code execution
# Flag: safetensors_used (INFO)
tensors = load_file("models/fashion_encoder.safetensors")
print("Loaded via safetensors (safe)")

# SAFE: torch.load with weights_only=True (PyTorch 2.0+)
# Flag: torch_load_safe (INFO)
state_dict = torch.load("checkpoints/model.pt", weights_only=True)
model = torch.nn.Linear(128, 64)
model.load_state_dict(state_dict)

# SAFE: ONNX runtime — no Python code in model file
# Flag: onnx_used (INFO)
sess = ort.InferenceSession("models/size_predictor.onnx")
print("ONNX model loaded (safe)")
