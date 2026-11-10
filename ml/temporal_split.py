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
        WHEN step <= 594 THEN 'TREINAMENTO'
        ELSE 'TESTE'
    END AS conjunto,
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

print("\n=== SENTINEL AI | DIVISÃO TEMPORAL ===")
print(df.to_string(index=False))

print("\nDivisão temporal validada!")
