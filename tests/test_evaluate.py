import pytest

from src.abstain import confidence, decide
from src.evaluate import aurc, recall_at_k, risk_coverage


def test_recall_at_k():
    retrieved = [{"doc": "phak", "page": 5}, {"doc": "afh", "page": 9}]
    assert recall_at_k(retrieved, "afh", 9, k=2) == 1.0
    assert recall_at_k(retrieved, "afh", 9, k=1) == 0.0


def test_confidence_and_decide():
    assert confidence([0.9, 0.6, 0.1], "top1") == pytest.approx(0.9)
    assert confidence([0.9, 0.6, 0.1], "margin") == pytest.approx(0.3)
    assert confidence([], "margin") == 0.0
    assert decide(0.5, 0.5) is True
    assert decide(0.4, 0.5) is False


def test_risk_coverage():
    curve = risk_coverage([0.9, 0.1, 0.5], [True, False, False])
    assert curve == [
        pytest.approx((1 / 3, 0.0)),
        pytest.approx((2 / 3, 0.5)),
        pytest.approx((1.0, 2 / 3)),
    ]
    assert aurc(curve) == pytest.approx((0.0 + 0.5 + 2 / 3) / 3)
