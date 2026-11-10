import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no arquivo .env")

engine = create_engine(DATABASE_URL)

query = """
SELECT
    step,
    type,
    amount,
    oldbalance_org,
    newbalance_orig,
    oldbalance_dest,
    newbalance_dest,
    is_fraud
FROM public.paysim_transactions
"""

print("Carregando dados do PostgreSQL...")

with engine.connect() as connection:
    df = pd.read_sql(text(query), connection)

print(f"Total de registros: {len(df):,}")

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"].astype(int)

X = pd.get_dummies(X, columns=["type"], dtype=int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Treinamento: {len(X_train):,} registros")
print(f"Teste: {len(X_test):,} registros")
print(f"Fraudes no treinamento: {y_train.sum():,}")
print(f"Fraudes no teste: {y_test.sum():,}")

print("Preparação concluída com sucesso!")
