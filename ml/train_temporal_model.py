import os
from pathlib import Path
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

columns = """
    step, type, amount,
    oldbalance_org, newbalance_orig,
    oldbalance_dest, newbalance_dest,
    is_fraud
"""

print("Carregando fraudes do período de treinamento...")

with engine.connect() as conn:
    fraudes = pd.read_sql(
        text(f"""
            SELECT {columns}
            FROM public.paysim_transactions
            WHERE step <= 594 AND is_fraud = TRUE
        """),
        conn
    )

    print("Carregando transações legítimas...")

    legitimas = pd.read_sql(
        text(f"""
            SELECT {columns}
            FROM public.paysim_transactions
            WHERE step <= 594 AND is_fraud = FALSE
            ORDER BY random()
            LIMIT 100000
        """),
        conn
    )

df = pd.concat([fraudes, legitimas], ignore_index=True)

X = pd.get_dummies(
    df.drop(columns=["is_fraud"]),
    columns=["type"],
    dtype=int
)
y = df["is_fraud"].astype(int)

print(f"Registros para treinamento: {len(df):,}")
print(f"Fraudes no treinamento: {y.sum():,}")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("Treinando modelo temporal...")
model.fit(X, y)

output = ROOT / "ml" / "sentinel_temporal_model.pkl"

joblib.dump(
    {"model": model, "features": X.columns.tolist()},
    output
)

print("Treinamento concluído com sucesso!")
print(f"Modelo salvo em: {output}")
