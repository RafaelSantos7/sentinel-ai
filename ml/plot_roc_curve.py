
from pathlib import Path
import os

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.metrics import roc_curve, roc_auc_score

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

print("Carregando dados para curva ROC...")

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

fpr, tpr, _ = roc_curve(y, probabilities)
auc = roc_auc_score(y, probabilities)

fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(
    fpr, tpr,
    color="#2563EB",
    linewidth=2,
    label=f"ROC-AUC = {auc:.4f}"
)

ax.plot(
    [0, 1], [0, 1],
    linestyle="--",
    color="gray",
    label="Classificador aleatório"
)

ax.set_title("Sentinel AI | Curva ROC", fontsize=15)
ax.set_xlabel("Taxa de falsos positivos")
ax.set_ylabel("Taxa de verdadeiros positivos")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.01)
ax.grid(alpha=0.3)
ax.legend(loc="lower right")

plt.tight_layout()

output = ROOT / "docs" / "figures"
output.mkdir(parents=True, exist_ok=True)

file_path = output / "roc_curve_final.png"

plt.savefig(file_path, dpi=300)
plt.close()

print("Curva ROC gerada com sucesso!")
print(f"Arquivo salvo em: {file_path}")
