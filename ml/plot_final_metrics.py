
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "ml" / "final_metrics.json", encoding="utf-8") as f:
    metrics = json.load(f)

names = [
    "Precisão",
    "Recall",
    "F1-Score",
    "Average Precision",
    "ROC-AUC"
]

values = [
    metrics["precision"],
    metrics["recall"],
    metrics["f1_score"],
    metrics["average_precision"],
    metrics["roc_auc"]
]

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(names, values, color="#2563EB")

ax.set_xlim(0, 1.1)
ax.set_xlabel("Pontuação")
ax.set_title("Sentinel AI | Métricas Finais", fontsize=16)
ax.invert_yaxis()

for bar, value in zip(bars, values):
    ax.text(
        value + 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2%}",
        va="center"
    )

plt.tight_layout()

output = ROOT / "docs" / "figures"
output.mkdir(parents=True, exist_ok=True)

file_path = output / "metricas_finais.png"

plt.savefig(file_path, dpi=300)
plt.close()

print("Gráfico de métricas gerado com sucesso!")
print(f"Arquivo salvo em: {file_path}")

