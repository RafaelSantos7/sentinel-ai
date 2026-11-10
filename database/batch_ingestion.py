import os
import random
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Localizar a raiz do projeto
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "database"))

from generate_transactions import generate_transaction

load_dotenv(ROOT / ".env")

TOTAL = 100

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    ) as conn:

        with conn.cursor() as cursor:
            inserted = 0

            for _ in range(TOTAL):
                customer_id = random.randint(1, 5)
                transaction = generate_transaction(customer_id)

                cursor.execute("""
                    INSERT INTO public.transactions (
                        source_transaction_id,
                        customer_id,
                        amount,
                        transaction_type,
                        transaction_date,
                        old_balance_origin,
                        new_balance_origin,
                        data_source,
                        is_fraud
                    )
                    VALUES (
                        %(source_transaction_id)s,
                        %(customer_id)s,
                        %(amount)s,
                        %(transaction_type)s,
                        %(transaction_date)s,
                        %(old_balance_origin)s,
                        %(new_balance_origin)s,
                        %(data_source)s,
                        FALSE
                    )
                    ON CONFLICT (
                        data_source,
                        source_transaction_id
                    ) DO NOTHING;
                """, transaction)

                inserted += cursor.rowcount

            cursor.execute("""
                INSERT INTO public.ingestion_logs (
                    source_name,
                    records_received,
                    records_inserted,
                    records_rejected,
                    status,
                    finished_at
                )
                VALUES (
                    'SYNTHETIC_BATCH',
                    %s,
                    %s,
                    %s,
                    'SUCCESS',
                    CURRENT_TIMESTAMP
                );
            """, (TOTAL, inserted, TOTAL - inserted))

        print("Ingestão em lote concluída!")
        print(f"Registros recebidos: {TOTAL}")
        print(f"Registros inseridos: {inserted}")
        print(f"Registros ignorados: {TOTAL - inserted}")

except Exception as erro:
    print(f"Erro na ingestão: {erro}")
