from src.rules_engine.rule_engine import evaluate_rules


def test_evaluate_rules_returns_list() -> None:
    result = evaluate_rules(fields={}, rules=[])
    assert isinstance(result, list)
