import uuid
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

TRANSACTION_TYPES = [
    "PIX",
    "TRANSFERENCIA",
    "PAGAMENTO",
    "SAQUE"
]


def generate_transaction(customer_id):
    transaction_type = random.choice(TRANSACTION_TYPES)

    amount = Decimal(str(round(
        random.uniform(10, 15000), 2
    )))

    old_balance = Decimal(str(round(
        random.uniform(100, 50000), 2
    )))

    new_balance = max(
        Decimal("0"),
        old_balance - amount
    )

    transaction_date = (
        datetime.now(timezone.utc)
        - timedelta(days=random.randint(0, 180))
    )

    return {
        "source_transaction_id": str(uuid.uuid4()),
        "customer_id": customer_id,
        "amount": amount,
        "transaction_type": transaction_type,
        "transaction_date": transaction_date,
        "old_balance_origin": old_balance,
        "new_balance_origin": new_balance,
        "data_source": "SYNTHETIC"
    }


if __name__ == "__main__":
    transaction = generate_transaction(1)
    print(transaction)
