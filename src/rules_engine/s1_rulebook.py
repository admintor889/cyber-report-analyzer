from typing import Dict, List


S1_RULEBOOK_VERSION = "S1-RULEBOOK-v0.1"

S1_P0_RULES: List[Dict[str, str]] = [
    {
        "rule_id": "S1-RSA-001",
        "name": "RSA key length baseline",
        "field": "crypto.rsa.key_length",
        "priority": "P0",
        "policy": ">=3072 PASS, ==2048 REVIEW, <2048 FAIL",
    },
    {
        "rule_id": "S1-TLS-001",
        "name": "TLS version baseline",
        "field": "crypto.tls.version",
        "priority": "P0",
        "policy": ">=1.2 PASS, ==1.1 REVIEW, <=1.0 FAIL",
    },
    {
        "rule_id": "S1-WEAK-001",
        "name": "Weak algorithm keyword baseline",
        "field": "crypto.weak",
        "priority": "P0",
        "policy": "Weak keyword hit => REVIEW, otherwise PASS",
    },
]


def get_s1_rulebook() -> Dict[str, object]:
    """Return S1 rulebook metadata used by baseline analysis path."""
    return {
        "rulebook_version": S1_RULEBOOK_VERSION,
        "rules": list(S1_P0_RULES),
    }
