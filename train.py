"""
1st Party Model Training — Myntra Style Recommender v3
Detection signals: trainer.train(), loss.backward(), DataLoader, optimizer, epochs
Asset type: 1st_party_model
"""
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.optim import AdamW
from transformers import (
    AutoTokenizer,
    AutoModel,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
from datasets import load_dataset, DatasetDict
from peft import LoraConfig, get_peft_model, TaskType
import numpy as np
from sklearn.metrics import ndcg_score


# ── Dataset ────────────────────────────────────────────────────────────────────

class MyntraStyleDataset(Dataset):
    """Paired (user_context, style_embedding) training samples."""

    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data[idx]
        encoding = self.tokenizer(
            row["style_description"],
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(row["user_engagement_score"], dtype=torch.float),
        }


# ── Model ──────────────────────────────────────────────────────────────────────

class StyleRecommender(nn.Module):
    """Fine-tuned encoder with engagement score prediction head."""

    def __init__(self, base_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(base_model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.encoder.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        pooled = self.dropout(pooled)
        logits = self.classifier(pooled).squeeze(-1)

        loss = None
        if labels is not None:
            criterion = nn.MSELoss()
            loss = criterion(logits, labels)

        return {"loss": loss, "logits": logits}


# ── Training Loop ──────────────────────────────────────────────────────────────

def train():
    # Config
    MODEL_NAME = os.getenv("BASE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./checkpoints/style-recommender-v3")
    epochs = int(os.getenv("EPOCHS", "5"))
    batch_size = int(os.getenv("BATCH_SIZE", "64"))
    learning_rate = float(os.getenv("LR", "2e-5"))

    print(f"Training StyleRecommender v3 | base={MODEL_NAME} | epochs={epochs}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = StyleRecommender(MODEL_NAME)

    # Apply LoRA for parameter-efficient fine-tuning
    lora_config = LoraConfig(
        task_type=TaskType.FEATURE_EXTRACTION,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["query", "value"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load and prepare dataset
    # Production: loads from internal feature store / BigQuery export
    raw_data = [
        {"style_description": "casual summer dress floral print", "user_engagement_score": 0.87},
        {"style_description": "formal blazer navy blue slim fit", "user_engagement_score": 0.72},
        # ... 1M+ samples in production
    ]

    train_size = int(0.9 * len(raw_data))
    train_data = MyntraStyleDataset(raw_data[:train_size], tokenizer)
    val_data = MyntraStyleDataset(raw_data[train_size:], tokenizer)

    train_dataset = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=4)
    val_dataset = DataLoader(val_data, batch_size=batch_size, num_workers=4)

    # HuggingFace Trainer
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        warmup_steps=500,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        report_to="none",
        fp16=torch.cuda.is_available(),
        dataloader_num_workers=4,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=val_data,
        tokenizer=tokenizer,
    )

    print("Starting training...")
    trainer.train()

    # Save final model
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Model saved to {OUTPUT_DIR}")


# ── Manual PyTorch Loop (alternative) ─────────────────────────────────────────

def train_manual_loop():
    """Lower-level training loop with explicit backward pass."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StyleRecommender().to(device)
    optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
    criterion = nn.MSELoss()

    # Dummy train_dataset for illustration
    train_dataset = []

    epochs = 5
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_dataset:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask, labels)
            loss = outputs["loss"]
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / max(len(train_dataset), 1)
        print(f"Epoch {epoch+1}/{epochs} — Loss: {avg_loss:.4f}")

    return model


if __name__ == "__main__":
    train()
