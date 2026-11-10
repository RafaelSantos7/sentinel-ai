import os
from pathlib import Path
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

artifact = joblib.load(
    ROOT / "ml" / "sentinel_final_model.pkl"
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
WHERE step BETWEEN 501 AND 594
"""

print("Carregando dados de validação...")

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

results = []

print("\n=== SENTINEL AI | VALIDAÇÃO DE THRESHOLDS ===")

for threshold in [0.3, 0.5, 0.6, 0.7, 0.8, 0.9]:
    predictions = (probabilities >= threshold).astype(int)

    precision = precision_score(y, predictions, zero_division=0)
    recall = recall_score(y, predictions, zero_division=0)
    f1 = f1_score(y, predictions, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(
        y, predictions, labels=[0, 1]
    ).ravel()

    results.append({
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "fp": fp,
        "fn": fn
    })

    print(
        f"Threshold: {threshold:.1f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f} | "
        f"FP: {fp} | FN: {fn}"
    )

best = max(results, key=lambda item: item["f1"])

config = {
    "threshold": best["threshold"],
    "selection_metric": "f1",
    "validation_steps": [501, 594]
}

joblib.dump(config, ROOT / "ml" / "threshold_config.pkl")

print("\n=== MELHOR THRESHOLD NA VALIDAÇÃO ===")
print(f"Threshold: {best['threshold']:.1f}")
print(f"F1-Score: {best['f1']:.3f}")
print("Configuração salva com sucesso!")
