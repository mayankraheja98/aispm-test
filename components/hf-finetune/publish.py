"""Fine-tune BERT for product classification and publish to HF Hub."""
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments)
from datasets import load_dataset
import torch

MODEL = "bert-base-multilingual-cased"
HUB_REPO = "myntra-fashion/product-classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=50)

dataset = load_dataset("myntra-org/product-titles")

training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=5,
    push_to_hub=True,
    hub_model_id=HUB_REPO,
)

trainer = Trainer(model=model, args=training_args, train_dataset=dataset["train"])
trainer.train()
trainer.push_to_hub()
model.push_to_hub(HUB_REPO)
tokenizer.push_to_hub(HUB_REPO)
print(f"Published to {HUB_REPO}")
