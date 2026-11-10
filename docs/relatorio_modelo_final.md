# Sentinel AI — Relatório Final do Modelo

Data de geração: 10/11/2026 19:59

## 1. Modelo

- Algoritmo: Random Forest
- Dataset: PaySim
- Estratégia: Divisão temporal
- Threshold: 0.7

## 2. Conjunto de teste

- Transações avaliadas: 123,580
- Fraudes existentes: 1,654

## 3. Métricas finais

- Acurácia: 99.70%
- Precisão: 95.99%
- Recall: 81.02%
- F1-Score: 87.87%
- Average Precision: 95.49%
- ROC-AUC: 99.91%

## 4. Matriz de confusão

- Verdadeiros negativos: 121870
- Falsos positivos: 56
- Falsos negativos: 314
- Verdadeiros positivos: 1340

## 5. Principais variáveis

- oldbalance_org: 27.50%
- newbalance_dest: 18.88%
- amount: 17.70%
- type_TRANSFER: 9.10%
- oldbalance_dest: 7.71%
- newbalance_orig: 7.68%
- step: 5.39%
- type_CASH_OUT: 2.62%
- type_CASH_IN: 1.82%
- type_PAYMENT: 1.58%

## 6. Considerações

O modelo apresentou desempenho promissor na identificação
de fraudes no conjunto de teste temporal.

Os resultados foram obtidos com dados simulados do PaySim
e não representam validação em ambiente bancário real.

Antes de uma aplicação em produção, são necessárias
avaliações adicionais de generalização, custos dos erros,
monitoramento e segurança.
