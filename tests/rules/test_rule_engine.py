from src.rules_engine.rule_engine import evaluate_rules


def test_evaluate_rules_returns_list() -> None:
    result = evaluate_rules(fields={}, rules=[])
    assert isinstance(result, list)


def test_evaluate_rules_numeric_comparison() -> None:
    fields = {"crypto.rsa.key_length": "2048"}
    rules = [
        {
            "rule_id": "R-RSA-001",
            "field": "crypto.rsa.key_length",
            "operator": ">=",
            "value": "3072",
        }
    ]
    result = evaluate_rules(fields=fields, rules=rules)
    assert result[0]["rule_id"] == "R-RSA-001"
    assert result[0]["verdict"] == "FAIL"


def test_evaluate_rules_missing_field_is_review() -> None:
    fields = {}
    rules = [
        {
            "rule_id": "R-TLS-001",
            "field": "crypto.tls.version",
            "operator": "==",
            "value": "1.2",
        }
    ]
    result = evaluate_rules(fields=fields, rules=rules)
    assert result[0]["verdict"] == "REVIEW"


def test_evaluate_rules_contains_pass() -> None:
    fields = {"crypto.weak": "algorithm md5 found"}
    rules = [
        {
            "rule_id": "R-WEAK-001",
            "field": "crypto.weak",
            "operator": "contains",
            "value": "md5",
        }
    ]
    result = evaluate_rules(fields=fields, rules=rules)
    assert result[0]["verdict"] == "PASS"
