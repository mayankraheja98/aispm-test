"""LoRA fine-tuning of LLaMA for fashion captioning."""
import torch
import wandb
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer

wandb.init(project="myntra-llm-finetune")

model_name = "meta-llama/Llama-3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, lora_config)

dataset = load_dataset("myntra-org/fashion-captions", split="train")

training_args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    save_steps=500,
    report_to="wandb",
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    dataset_text_field="text",
)
trainer.train()
model.save_pretrained("./final-model")
tokenizer.save_pretrained("./final-model")
