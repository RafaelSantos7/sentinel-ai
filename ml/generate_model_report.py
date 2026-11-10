
import json
from pathlib import Path
from datetime import datetime

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

with open(
    ROOT / "ml" / "final_metrics.json",
    encoding="utf-8"
) as file:
    metrics = json.load(file)

artifact = joblib.load(
    ROOT / "ml" / "sentinel_final_model.pkl"
)

model = artifact["model"]
features = artifact["features"]

importance = pd.DataFrame({
    "variavel": features,
    "importancia": model.feature_importances_
}).sort_values("importancia", ascending=False)

tn, fp = metrics["confusion_matrix"][0]
fn, tp = metrics["confusion_matrix"][1]

report = f"""# Sentinel AI — Relatório Final do Modelo

Data de geração: {datetime.now():%d/%m/%Y %H:%M}

## 1. Modelo
- Algoritmo: Random Forest
- Dataset: PaySim
- Estratégia: Divisão temporal
- Threshold: {metrics['threshold']}

## 2. Conjunto de teste
- Transações avaliadas: {metrics['total_transactions']:,}
- Fraudes existentes: {metrics['total_frauds']:,}

## 3. Métricas finais
- Acurácia: {metrics['accuracy']:.2%}
- Precisão: {metrics['precision']:.2%}
- Recall: {metrics['recall']:.2%}
- F1-Score: {metrics['f1_score']:.2%}
- Average Precision: {metrics['average_precision']:.2%}
- ROC-AUC: {metrics['roc_auc']:.2%}

## 4. Matriz de confusão
- Verdadeiros negativos: {tn}
- Falsos positivos: {fp}
- Falsos negativos: {fn}
- Verdadeiros positivos: {tp}

## 5. Principais variáveis
"""

for _, row in importance.head(10).iterrows():
    report += (
        f"- {row['variavel']}: "
        f"{row['importancia']:.2%}\n"
    )

report += """
## 6. Considerações
O modelo apresentou desempenho promissor na identificação
de fraudes no conjunto de teste temporal.

Os resultados foram obtidos com dados simulados do PaySim
e não representam validação em ambiente bancário real.

Antes de uma aplicação em produção, são necessárias
avaliações adicionais de generalização, custos dos erros,
monitoramento e segurança.
"""

output = ROOT / "docs" / "relatorio_modelo_final.md"
output.parent.mkdir(parents=True, exist_ok=True)

output.write_text(report, encoding="utf-8")

print("Relatório final gerado com sucesso!")
print(f"Arquivo salvo em: {output}")
