from .authorization_rules import (
    check_missing_rule,
    check_cross_player_modification,
    check_privileged_remote
)

from .exploit_rules import(
    check_negative_value_abuse,
    check_remote_spam,
    check_client_controlled_damage
)
SEVERITY_MESAURE = {
    "Critical": 25,
    "High": 15,
    "Medium": 10,
    "Low": 5,
}
RULES = [
    check_missing_rule,
    check_cross_player_modification,
    check_privileged_remote,
    check_negative_value_abuse,
    check_remote_spam,
    check_client_controlled_damage
]



def calculate_score(issues):
    score =100
    for issues in issues:
        severity = issues["severity"]
        measure = SEVERITY_MESAURE.get(severity,0)
        score -= measure
    
    return max (score,0)

def scan_code (code):
    issues =[]
    for rule in RULES:
        result = rule (code)

        if result:
            issues.append(result)

    score =calculate_score(issues)

    return issues, score