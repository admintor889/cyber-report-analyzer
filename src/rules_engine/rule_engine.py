from typing import Dict, List


VERDICTS = {"PASS", "FAIL", "REVIEW"}


def _to_float(value: str) -> float:
    return float(str(value).strip())


def _evaluate(operator: str, actual: str, expected: str) -> bool:
    operator = operator.strip()

    if operator in {">", ">=", "<", "<="}:
        left = _to_float(actual)
        right = _to_float(expected)
        if operator == ">":
            return left > right
        if operator == ">=":
            return left >= right
        if operator == "<":
            return left < right
        return left <= right

    if operator == "==":
        return str(actual).strip().lower() == str(expected).strip().lower()
    if operator == "!=":
        return str(actual).strip().lower() != str(expected).strip().lower()
    if operator == "contains":
        return str(expected).strip().lower() in str(actual).strip().lower()
    if operator == "not_contains":
        return str(expected).strip().lower() not in str(actual).strip().lower()

    raise ValueError(f"unsupported operator: {operator}")


def evaluate_rules(fields: Dict[str, str], rules: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Evaluate structured fields against configured rules.

    Rule format:
    - rule_id: unique rule id
    - field: source key in fields
    - operator: one of >, >=, <, <=, ==, !=, contains, not_contains
    - value: expected value for comparison
    """
    if not isinstance(fields, dict):
        raise TypeError("fields must be a dict")
    if not isinstance(rules, list):
        raise TypeError("rules must be a list")

    results: List[Dict[str, str]] = []

    for index, rule in enumerate(rules, start=1):
        if not isinstance(rule, dict):
            raise TypeError("each rule must be a dict")

        rule_id = str(rule.get("rule_id") or f"RULE-{index:03d}")
        field = str(rule.get("field") or "")
        operator = str(rule.get("operator") or "")
        expected = str(rule.get("value") or "")

        if not field:
            results.append(
                {
                    "rule_id": rule_id,
                    "field": "",
                    "value": "",
                    "verdict": "REVIEW",
                    "reason": "Rule field is missing.",
                }
            )
            continue

        if field not in fields:
            results.append(
                {
                    "rule_id": rule_id,
                    "field": field,
                    "value": "",
                    "verdict": "REVIEW",
                    "reason": "Field value is missing in extracted fields.",
                }
            )
            continue

        actual = str(fields[field])

        try:
            matched = _evaluate(operator, actual, expected)
            verdict = "PASS" if matched else "FAIL"
            reason = f"Rule comparison {actual} {operator} {expected} -> {matched}."
        except ValueError as ex:
            verdict = "REVIEW"
            reason = str(ex)
        except Exception:
            verdict = "REVIEW"
            reason = "Rule evaluation failed and requires manual review."

        results.append(
            {
                "rule_id": rule_id,
                "field": field,
                "value": actual,
                "verdict": verdict,
                "reason": reason,
            }
        )

    return results
