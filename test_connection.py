
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    ) as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user;")
            banco, usuario = cursor.fetchone()

            print("Conexão realizada com sucesso!")
            print(f"Banco de dados: {banco}")
            print(f"Usuário: {usuario}")

            cursor.execute("SELECT COUNT(*) FROM public.transactions;")
            total = cursor.fetchone()[0]

            print(f"Total de transações: {total}")

except Exception as erro:
    print(f"Erro ao conectar ao PostgreSQL: {erro}")
