
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from eda_paysim import df

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "figures"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Gráfico 1 — Distribuição das transações
totais = df.groupby("type")["total"].sum().sort_values()

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(totais.index, totais.values, color="#2563EB")
ax.set_title("Sentinel AI | Transações por tipo", fontsize=16)
ax.set_xlabel("Quantidade de transações")
ax.ticklabel_format(style="plain", axis="x")
fig.tight_layout()
fig.savefig(OUTPUT / "transacoes_por_tipo.png", dpi=200)
plt.close(fig)

# Gráfico 2 — Fraudes por tipo de transação
fraudes = df[df["is_fraud"] == True].set_index("type")["total"]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(fraudes.index, fraudes.values, color="#EF4444")
ax.set_title("Sentinel AI | Fraudes por tipo", fontsize=16)
ax.set_ylabel("Quantidade de fraudes")
fig.tight_layout()
fig.savefig(OUTPUT / "fraudes_por_tipo.png", dpi=200)
plt.close(fig)

print("Gráficos gerados com sucesso!")
print(f"Arquivos salvos em: {OUTPUT}")
