import os
from pathlib import Path
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
    roc_auc_score
)

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

artifact = joblib.load(
    ROOT / "ml" / "sentinel_final_model.pkl"
)

model = artifact["model"]
features = artifact["features"]

config = joblib.load(
    ROOT / "ml" / "threshold_config.pkl"
)

threshold = config["threshold"]

query = """
SELECT
    step, type, amount,
    oldbalance_org, newbalance_orig,
    oldbalance_dest, newbalance_dest,
    is_fraud
FROM public.paysim_transactions
WHERE step BETWEEN 595 AND 743
"""

print("Carregando dados do teste final...")

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
predictions = (probabilities >= threshold).astype(int)

print("\n=== SENTINEL AI | AVALIAÇÃO FINAL ===")
print(f"Threshold utilizado: {threshold}")
print(f"Transações avaliadas: {len(df):,}")
print(f"Fraudes existentes: {int(y.sum()):,}")

print("\nRelatório de classificação:")
print(classification_report(y, predictions, digits=4))

print("Matriz de confusão:")
print(confusion_matrix(y, predictions))

print("\nAverage Precision:")
print(f"{average_precision_score(y, probabilities):.4f}")

print("\nROC-AUC:")
print(f"{roc_auc_score(y, probabilities):.4f}")

print("\nAvaliação final concluída!")


import json
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

results = {
    "threshold": float(threshold),
    "total_transactions": int(len(df)),
    "total_frauds": int(y.sum()),
    "accuracy": float(accuracy_score(y, predictions)),
    "precision": float(precision_score(y, predictions)),
    "recall": float(recall_score(y, predictions)),
    "f1_score": float(f1_score(y, predictions)),
    "average_precision": float(
        average_precision_score(y, probabilities)
    ),
    "roc_auc": float(roc_auc_score(y, probabilities)),
    "confusion_matrix": confusion_matrix(
        y, predictions
    ).tolist()
}

output = ROOT / "ml" / "final_metrics.json"

with open(output, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print(f"\nMétricas salvas em: {output}")
