import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METRICS_PATH = ROOT / "ml" / "final_metrics.json"


def test_metrics_file_exists():
    assert METRICS_PATH.exists()


def test_final_metrics_values():
    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        metrics = json.load(file)

    assert isinstance(metrics, dict)
    assert "confusion_matrix" in metrics

    cm = metrics["confusion_matrix"]

    assert len(cm) == 2
    assert all(len(row) == 2 for row in cm)
    assert all(
        isinstance(value, int) and value >= 0
        for row in cm
        for value in row
    )
