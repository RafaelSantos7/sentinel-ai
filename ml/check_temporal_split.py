
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
    MIN(step) AS primeiro_step,
    MAX(step) AS ultimo_step,
    COUNT(*) AS total_transacoes,
    COUNT(*) FILTER (
        WHERE is_fraud = TRUE
    ) AS total_fraudes,
    COUNT(DISTINCT step) AS steps_distintos
FROM public.paysim_transactions
"""

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

print("\n=== SENTINEL AI | ANÁLISE TEMPORAL ===")
print(df.to_string(index=False))

print("\nAnálise temporal concluída!")
