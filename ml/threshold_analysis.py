
import os
from pathlib import Path

import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.metrics import precision_score, recall_score, f1_score

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

artifact = joblib.load(
    ROOT / "ml" / "sentinel_temporal_model.pkl"
)

model = artifact["model"]
features = artifact["features"]

query = """
SELECT
    step, type, amount,
    oldbalance_org, newbalance_orig,
    oldbalance_dest, newbalance_dest,
    is_fraud
FROM public.paysim_transactions
WHERE step > 594
"""

print("Carregando transações para análise...")

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

X = pd.get_dummies(
    df.drop(columns=["is_fraud"]),
    columns=["type"],
    dtype=int
)

X = X.reindex(columns=features, fill_value=0)
y = df["is_fraud"].astype(int)

probabilities = model.predict_proba(X)[:, 1]

print("\n=== SENTINEL AI | ANÁLISE DE THRESHOLDS ===")

for threshold in [0.3, 0.5, 0.6, 0.7, 0.8, 0.9]:
    predictions = (probabilities >= threshold).astype(int)

    precision = precision_score(y, predictions, zero_division=0)
    recall = recall_score(y, predictions, zero_division=0)
    f1 = f1_score(y, predictions, zero_division=0)

    false_positives = ((predictions == 1) & (y == 0)).sum()
    false_negatives = ((predictions == 0) & (y == 1)).sum()

    print(
        f"Threshold: {threshold:.1f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f} | "
        f"FP: {false_positives} | "
        f"FN: {false_negatives}"
    )

print("\nAnálise concluída!")
