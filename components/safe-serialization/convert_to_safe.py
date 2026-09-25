"""Convert existing pytorch model to safetensors format."""
import torch
from safetensors.torch import save_file
from transformers import AutoModel

model = AutoModel.from_pretrained("./checkpoints")
state_dict = model.state_dict()

# Save as safetensors instead of pickle-based .bin
save_file(state_dict, "models/fashion_encoder.safetensors")
print("Saved as safetensors (safe format)")
