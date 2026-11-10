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

print("Carregando dados do período de teste...")

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

X = pd.get_dummies(
    df.drop(columns=["is_fraud"]),
    columns=["type"],
    dtype=int
)

X = X.reindex(columns=features, fill_value=0)
y = df["is_fraud"].astype(int)

predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]

print("\n=== SENTINEL AI | AVALIAÇÃO TEMPORAL ===")
print(f"Transações avaliadas: {len(df):,}")
print(f"Fraudes existentes: {y.sum():,}")

print("\nRelatório de classificação:")
print(classification_report(y, predictions, zero_division=0))

print("\nMatriz de confusão:")
print(confusion_matrix(y, predictions))

print("\nAverage Precision:")
print(round(average_precision_score(y, probabilities), 4))

print("\nROC-AUC:")
print(round(roc_auc_score(y, probabilities), 4))

print("\nAvaliação temporal concluída!")
