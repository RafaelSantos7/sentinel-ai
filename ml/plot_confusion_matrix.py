import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

ROOT = Path(__file__).resolve().parent.parent

metrics_path = ROOT / "ml" / "final_metrics.json"

with open(metrics_path, "r", encoding="utf-8") as file:
    metrics = json.load(file)

cm = np.array(metrics["confusion_matrix"])

fig, ax = plt.subplots(figsize=(8, 6))

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Legítima", "Fraude"]
)

display.plot(
    ax=ax,
    cmap="Blues",
    values_format="d",
    colorbar=False
)

ax.set_title(
    "Sentinel AI | Matriz de Confusão",
    fontsize=15
)

ax.set_xlabel("Classificação prevista")
ax.set_ylabel("Classificação real")

plt.tight_layout()

output = ROOT / "docs" / "figures"
output.mkdir(parents=True, exist_ok=True)

file_path = output / "matriz_confusao_final.png"

plt.savefig(file_path, dpi=300)
plt.close()

print("Matriz de confusão gerada com sucesso!")
print(f"Arquivo salvo em: {file_path}")
