import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER", "sentinel_app"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "sentinel_ai"),
)

engine = create_engine(url)

query = text("""
    SELECT
        type,
        is_fraud,
        COUNT(*) AS total,
        ROUND(AVG(amount), 2) AS valor_medio
    FROM public.paysim_transactions
    GROUP BY type, is_fraud
    ORDER BY type, is_fraud
""")

with engine.connect() as connection:
    df = pd.read_sql(query, connection)

print("\n=== SENTINEL AI | ANÁLISE EXPLORATÓRIA ===")
print(df.to_string(index=False))
print("\nAnálise concluída com sucesso!")

engine.dispose()
