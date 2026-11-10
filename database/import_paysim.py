import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from tqdm import tqdm

# Configurações
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "database" / "data"
CHUNK_SIZE = 10000

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

csv_files = list(DATA_DIR.glob("PS_20174392719_1491204439457_log.csv"))

if not csv_files:
    raise FileNotFoundError("Arquivo CSV do PaySim não encontrado.")

csv_path = csv_files[0]

columns = {
    "nameOrig": "name_orig",
    "oldbalanceOrg": "oldbalance_org",
    "newbalanceOrig": "newbalance_orig",
    "nameDest": "name_dest",
    "oldbalanceDest": "oldbalance_dest",
    "newbalanceDest": "newbalance_dest",
    "isFraud": "is_fraud",
    "isFlaggedFraud": "is_flagged_fraud",
}

total = 0

for chunk in tqdm(
    pd.read_csv(csv_path, chunksize=CHUNK_SIZE),
    desc="Importando PaySim",
    unit="lote",
):
    chunk = chunk.rename(columns=columns)

    chunk["is_fraud"] = chunk["is_fraud"].astype(bool)
    chunk["is_flagged_fraud"] = chunk["is_flagged_fraud"].astype(bool)

    chunk.to_sql(
        "paysim_transactions",
        engine,
        schema="public",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    total += len(chunk)

print(f"Importação concluída! Registros importados: {total:,}")
