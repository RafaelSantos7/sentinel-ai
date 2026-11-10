import os
import uuid
from datetime import datetime, timezone

import psycopg
from dotenv import load_dotenv

load_dotenv()

# Identificador de teste para evitar duplicações
source_name = f"sentinel_test_{uuid.uuid4().hex[:8]}"

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    ) as conn:

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.transactions
                    (customer_id, amount, transaction_type,
                     transaction_date, is_fraud)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING transaction_id;
            """, (
                1,
                750.00,
                "PIX",
                datetime.now(timezone.utc),
                False
            ))

            transaction_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO public.ingestion_logs
                    (source_name, records_received,
                     records_inserted, records_rejected,
                     status, finished_at)
                VALUES (%s, 1, 1, 0, 'SUCCESS', CURRENT_TIMESTAMP);
            """, (source_name,))

        print("Ingestão realizada com sucesso!")
        print(f"Transação criada: {transaction_id}")
        print("Registros inseridos: 1")

except Exception as erro:
    print(f"Erro durante a ingestão: {erro}")
