
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

artifact = joblib.load(
    ROOT / "ml" / "sentinel_final_model.pkl"
)

model = artifact["model"]
features = artifact["features"]

importance = pd.DataFrame({
    "variavel": features,
    "importancia": model.feature_importances_
})

importance = importance.sort_values(
    "importancia", ascending=False
).head(15)

fig, ax = plt.subplots(figsize=(11, 7))

ax.barh(
    importance["variavel"][::-1],
    importance["importancia"][::-1],
    color="#2563EB"
)

ax.set_title(
    "Sentinel AI | Importância das Variáveis",
    fontsize=16
)
ax.set_xlabel("Importância no Random Forest")
ax.set_ylabel("Variáveis")
ax.grid(axis="x", alpha=0.2)

plt.tight_layout()

output = ROOT / "docs" / "figures"
output.mkdir(parents=True, exist_ok=True)

file_path = output / "feature_importance_final.png"

plt.savefig(file_path, dpi=300)
plt.close()

print("Gráfico de importância gerado com sucesso!")
print(f"Arquivo salvo em: {file_path}")

print("\nPrincipais variáveis:")
print(importance.to_string(index=False))
