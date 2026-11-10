import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METRICS_PATH = ROOT / "ml" / "final_metrics.json"


def test_confusion_matrix_total():
    with open(METRICS_PATH, encoding="utf-8") as file:
        metrics = json.load(file)

    cm = metrics["confusion_matrix"]

    total = sum(sum(row) for row in cm)

    assert total == 123580


def test_confusion_matrix_fraud_counts():
    with open(METRICS_PATH, encoding="utf-8") as file:
        metrics = json.load(file)

    cm = metrics["confusion_matrix"]

    false_negatives = cm[1][0]
    true_positives = cm[1][1]

    assert false_negatives + true_positives == 1654
