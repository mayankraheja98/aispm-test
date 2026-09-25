# Myntra Style Recommender — Model Training
Fine-tuned sentence encoder for fashion recommendation scoring.
Trained on Myntra's user engagement data (click-through, purchase, dwell time).

**Asset type:** 1st Party Model
**Base model:** sentence-transformers/all-MiniLM-L6-v2
**Training:** LoRA fine-tuning on Myntra engagement dataset (~2M samples)
**Output:** style-recommender-v3 (pushed to internal model registry)
**Schedule:** Retraining triggered weekly if NDCG < 0.80
