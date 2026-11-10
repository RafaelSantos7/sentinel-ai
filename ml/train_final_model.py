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

print("=== SENTINEL AI | TREINAMENTO FINAL ===")

with engine.connect() as conn:
    print("Carregando fraudes do treinamento...")

    fraudes = pd.read_sql(
        text(f"""
            SELECT {columns}
            FROM public.paysim_transactions
            WHERE step BETWEEN 1 AND 500
              AND is_fraud = TRUE
        """),
        conn
    )

    print("Carregando transações legítimas...")

    legitimas = pd.read_sql(
        text(f"""
            SELECT {columns}
            FROM public.paysim_transactions
            WHERE step BETWEEN 1 AND 500
              AND is_fraud = FALSE
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

print(f"Transações utilizadas: {len(df):,}")
print(f"Fraudes utilizadas: {y.sum():,}")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

print("Treinando Random Forest...")
model.fit(X, y)

output = ROOT / "ml" / "sentinel_final_model.pkl"

joblib.dump(
    {
        "model": model,
        "features": X.columns.tolist(),
        "training_steps": [1, 500]
    },
    output
)

print("\nTreinamento concluído com sucesso!")
print(f"Modelo salvo em: {output}")
