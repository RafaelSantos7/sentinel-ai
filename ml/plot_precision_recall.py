
from pathlib import Path
import os

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.metrics import precision_recall_curve, average_precision_score

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

artifact = joblib.load(ROOT / "ml" / "sentinel_final_model.pkl")
model = artifact["model"]
features = artifact["features"]

query = """
SELECT
    step, type, amount,
    oldbalance_org, newbalance_orig,
    oldbalance_dest, newbalance_dest,
    is_fraud
FROM public.paysim_transactions
WHERE step BETWEEN 595 AND 743
"""

print("Carregando dados para curva Precision-Recall...")

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

precision, recall, _ = precision_recall_curve(
    y, probabilities
)

ap = average_precision_score(y, probabilities)

fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(recall, precision, color="#2563EB", linewidth=2)
ax.set_title("Sentinel AI | Curva Precision-Recall", fontsize=15)
ax.set_xlabel("Recall")
ax.set_ylabel("Precisão")
ax.set_xlim(0, 1.01)
ax.set_ylim(0, 1.01)
ax.grid(alpha=0.3)

ax.legend([f"Average Precision = {ap:.4f}"])

plt.tight_layout()

output = ROOT / "docs" / "figures"
output.mkdir(parents=True, exist_ok=True)

file_path = output / "precision_recall_final.png"
plt.savefig(file_path, dpi=300)
plt.close()

print("Curva Precision-Recall gerada com sucesso!")
print(f"Arquivo salvo em: {file_path}")
