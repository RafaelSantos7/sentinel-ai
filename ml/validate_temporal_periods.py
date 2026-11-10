import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

query = """
SELECT
    CASE
        WHEN step <= 500 THEN '1 - TREINAMENTO'
        WHEN step <= 594 THEN '2 - VALIDACAO'
        ELSE '3 - TESTE FINAL'
    END AS conjunto,
    MIN(step) AS primeiro_step,
    MAX(step) AS ultimo_step,
    COUNT(*) AS total_transacoes,
    COUNT(*) FILTER (
        WHERE is_fraud = TRUE
    ) AS total_fraudes
FROM public.paysim_transactions
GROUP BY 1
ORDER BY 1
"""

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

df["taxa_fraude_pct"] = (
    df["total_fraudes"] /
    df["total_transacoes"] * 100
).round(4)

print("\n=== SENTINEL AI | DIVISAO FINAL ===")
print(df.to_string(index=False))
print("\nValidacao dos periodos concluida!")
