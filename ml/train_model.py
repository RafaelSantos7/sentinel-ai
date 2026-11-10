import os
from pathlib import Path
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"])

query = """
SELECT
    step, type, amount,
    oldbalance_org, newbalance_orig,
    oldbalance_dest, newbalance_dest,
    is_fraud
FROM public.paysim_transactions
"""

print("Carregando amostra para treinamento...")

# Amostra estratificada: inclui fraudes e transações legítimas
with engine.connect() as conn:
    fraudes = pd.read_sql(
        text(query + " WHERE is_fraud = TRUE"),
        conn
    )

    legitimas = pd.read_sql(
        text(query + """
            WHERE is_fraud = FALSE
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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2,
    random_state=42, stratify=y
)

print("Treinando Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\n=== RESULTADOS DO MODELO ===")
print(classification_report(y_test, predictions, zero_division=0))

output = ROOT / "ml" / "sentinel_model.pkl"
joblib.dump(
    {"model": model, "features": X.columns.tolist()},
    output
)

print(f"\nModelo salvo em: {output}")
